import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from first.models import Voting, VoteVariant, VoteFact, Complaint, ProfilePhoto


def voting_page(request, voting_id):
    """
        Обработчик страницы голосования

        :param request: объект с деталями HTTP-запроса
        :param voting_id: id голосования
        :return: Объект с деталями HTTP-ответа
    """

    class Progress:
        def __init__(self, color, procent):
            self.color = color
            self.procent = procent

    context = {}
    context["all_votes_count"] = 0
    votes_percent = []
    obj_arr = []
    colors_styles = ["progress-bar", "progress-bar bg-success", "progress-bar bg-info", "progress-bar bg-warning",
                     "progress-bar bg-danger"]
    variant_colors = []
    context["pagetitle"] = "Голосование"
    context["pageheader"] = "Было два стула"
    context['voting'] = get_object_or_404(Voting, id=voting_id)
    context["voting_variants"] = VoteVariant.objects.filter(voting=voting_id)
    context['styles'] = colors_styles[:len(context["voting_variants"])]
    for el in VoteVariant.objects.filter(voting=voting_id):
        context["all_votes_count"] += el.votes_count
    for i in range(len(VoteVariant.objects.filter(voting=voting_id))):
        if context["all_votes_count"] > 0:
            obj_arr.append(Progress(colors_styles[random.randint(0, 4)],
                                    VoteVariant.objects.filter(voting=voting_id)[i].votes_count / context[
                                        "all_votes_count"] * 100))
        else:
            obj_arr.append(Progress(colors_styles[random.randint(0, 4)], 0))

    if request.user.is_authenticated:
        is_voted = False
        for votefact in VoteFact.objects.filter(author=request.user):
            if VoteVariant.objects.filter(id=votefact.variant_id).filter(voting_id=voting_id).count() != 0:
                is_voted = True
                context["is_voted"] = is_voted
                break
    else:
        hello = "hello, world"
        print(hello)
        print("100th commit!!!")
        is_voted = True
        context["is_voted"] = is_voted

    if request.method == "POST":
        print(request.POST)
        if request.user.is_authenticated and not is_voted:
            for var_id in request.POST.getlist('variant_id'):
                record = VoteFact(variant_id=int(var_id),
                                  created_at=datetime.datetime.now(),
                                  author=request.user)
                record.save()
            context["is_voted"] = True
            return redirect(f"/voting/{context['voting'].id}")

    context["colors"] = variant_colors
    context["votes_percent"] = votes_percent
    context["progress"] = obj_arr

    return render(request, 'voting.html', context)


def list_of_votings_page(request):
    """
        Обработчик страницы списка голосований

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    context["pagetitle"] = "List of votings"
    context["pageheader"] = "Все голосования"
    context["votings_list"] = Voting.objects.all()
    return render(request, 'list_of_votings.html', context)


def index_page(request):
    """
        Обработчик начальной страницы

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    context["pagetitle"] = "Index page"
    context["pageheader"] = "Главная"
    return render(request, 'index.html', context)


@login_required(login_url='/registration/')
def add_voting(request):
    """
        Обработчик страницы добавления голосования

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    if request.method == "POST":
        if int(request.POST['voting_type']) and request.POST['theme'] and request.POST.get(
                "variants") and request.user.is_authenticated and request.POST['description']:
            try:
                new_voting = Voting(
                    name=request.POST['theme'],
                    description=request.POST['description'],
                    voting_type=int(request.POST['voting_type']),
                    author=request.user,
                    image=request.FILES['image'],
                )
            except:
                new_voting = Voting(
                    name=request.POST['theme'],
                    description=request.POST['description'],
                    voting_type=int(request.POST['voting_type']),
                    author=request.user,
                )

            new_voting.save()
            for variant in request.POST.getlist("variants"):
                new_variant = VoteVariant(
                    description=variant,
                    voting=new_voting,
                )
                new_variant.save()
            return redirect(f"/voting/{new_voting.id}")

    return render(request, 'add_voting.html', context)


def registration(request):
    """
        Обработчик страницы регистрации

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    context["pagetitle"] = "Registration"
    context["pageheader"] = "Регистрация"
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            context['form'] = form
            messages.add_message(request, messages.SUCCESS, "Новый пользователь создан")
        else:
            form = UserCreationForm()
            context['form'] = form
            messages.add_message(request, messages.ERROR, "Введены некорректные данные")
    else:
        form = UserCreationForm()
        context['form'] = form
    return render(request, 'registration/registrarion.html', context)


@login_required(login_url='/registration/')
def redact_voting(request, voting_id):
    """
        Обработчик страницы редактирования голосования

        :param request: объект с деталями HTTP-запроса
        :param voting_id: id голосования для редактирования
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    context['voting'] = get_object_or_404(Voting, id=voting_id)
    context['variants'] = VoteVariant.objects.filter(voting_id=voting_id)
    if request.method == "POST":
        print(request.POST)
        voting_tochange = Voting.objects.get(id=voting_id)
        if request.POST['theme'] != context['voting'].name:
            voting_tochange.name = request.POST['theme']

        if request.POST['description'] != context['voting'].description:
            voting_tochange.description = request.POST['description']

        voting_tochange.save()
        variants = []
        for key, value in request.POST.items():
            if key[:7] == "variant":
                variants.append((request.POST[key], int(key[8:])))
        print(variants)
        for variant in variants:
            if not variant[0]:
                VoteVariant.objects.get(id=variant[1]).delete()
            elif variant[0] != VoteVariant.objects.get(id=variant[1]).description:
                new_variant = VoteVariant.objects.get(id=variant[1])
                new_variant.description = variant[0]
                new_variant.save()

    else:
        for variant in context['variants']:
            if VoteFact.objects.filter(variant=variant.id).count() != 0:
                return redirect("/list/")

        if context['voting'].author != request.user:
            return redirect("/list/")

    return render(request, 'redact_voting.html', context)

@login_required(login_url='/registration/')
def profile(request, profile_id):
    """
        Страница профиля пользователя

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    profile = User.objects.get(id=profile_id)
    context["votings"] = Voting.objects.filter(author=profile_id)
    context["votefacts"] = VoteFact.objects.filter(author=profile_id)
    context["profile"] = profile
    context["profile"] = User.objects.get(id=profile_id)
    try:
        profile_photo = ProfilePhoto.objects.get(user_id=profile_id)
        print(profile_photo.image)
        context["photo"] = profile_photo.image
    except:
        context["photo"] = "basic_profile_image.png"
    return render(request, "profile.html", context)

@login_required(login_url='/registration/')
def redact_profile(request, redact_profile_id):
    """
        Обработчик страницы редактирования профиля

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    if request.method == "POST":
        profile = User.objects.get(id=redact_profile_id)
        context["profile"] = profile
        profile.last_name = request.POST["last_name"]
        profile.email = request.POST["email"]
        profile.save()
        try:
            upload_photo = request.FILES['image']
            try:
                profile_photo = ProfilePhoto.objects.get(user_id=redact_profile_id)
                profile_photo.image = upload_photo
                profile_photo.save()
            except:
                new_photo = ProfilePhoto(
                    user_id=redact_profile_id,
                    image=upload_photo
                )
                new_photo.save()
        except:
            print('No photo uploaded')

        try:
            profile_photo = ProfilePhoto.objects.get(user_id=redact_profile_id)
            print(profile_photo.image)
            context["photo"] = profile_photo.image
        except:
            context["photo"] = "basic_profile_image.png"

    elif request.method == "GET":
        context["profile"] = User.objects.get(id=redact_profile_id)
        try:
            profile_photo = ProfilePhoto.objects.get(user_id=redact_profile_id)
            print(profile_photo.image)
            context["photo"] = profile_photo.image
        except:
            context["photo"] = "basic_profile_image.png"
    return render(request, "redact_profile.html", context)


@login_required(login_url='/registration/')
def complaint(request):
    context = {}
    if request.method == "POST":
        if request.POST.get('title') and request.POST.get('description'):
            complaint = Complaint(
                name=request.POST['title'],
                description=request.POST['description'],
                author=request.user,
                created_at=datetime.datetime.now()
            )
            complaint.save()
    return render(request, "complaint.html", context)

# Create your views here.
