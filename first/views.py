import datetime
import random

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from first.models import Voting, VoteVariant, VoteFact


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
    if request.method == "POST":
        is_voted = False
        for votefact in VoteFact.objects.filter(author=request.user):
            if VoteVariant.objects.filter(id=votefact.variant_id).filter(voting_id=voting_id).count() != 0:
                is_voted = True
                context["is_voted"] = is_voted
                break
        print(request.POST)
        if request.user.is_authenticated and not is_voted:
            for var_id in request.POST.getlist('variant_id'):
                record = VoteFact(variant_id=int(var_id),
                                  created_at=datetime.datetime.now(),
                                  author=request.user)
                record.save()

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
            new_voting = Voting(
                name=request.POST['theme'],
                description=request.POST['description'],
                voting_type=int(request.POST['voting_type']),
                author=request.user,
                image=request.FILES['image'],
            )

            new_voting.save()
            for variant in request.POST.getlist("variants"):
                new_variant = VoteVariant(
                    description=variant,
                    voting=new_voting,
                )
                new_variant.save()

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
        if (int(request.POST['voting_type']) or request.POST['theme'] or request.POST.get(
                "variants") or request.POST['description']) and context['voting'].author == request.user:
            voting_tochange = Voting.objects.get(id=voting_id)
            voting_tochange.voting_type = int(request.POST['voting_type'])
            voting_tochange.name = request.POST['theme']
            voting_tochange.description = request.POST['description']
            voting_tochange.save()
            flag = True
            for variant in request.POST.getlist("variants"):
                if not variant:
                    flag = False
            if flag:
                VoteVariant.objects.filter(voting_id=voting_id).delete()
                for variant in request.POST.getlist("variants"):
                    new_variant = VoteVariant(
                        description=variant,
                        voting=voting_tochange,
                    )
                    new_variant.save()

    return render(request, 'redact_voting.html', context)


def profile(request, profile_id):
    """
        Страница профиля пользователя

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    profile = User.objects.get(id=profile_id)
    context["votings"] = Voting.objects.filter(author = profile_id)
    context["votefacts"] = VoteFact.objects.filter(author=profile_id)
    context["profile"] = profile
    return render(request, "profile.html", context)


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
    elif request.method == "GET":
        context["profile"] = User.objects.get(id=redact_profile_id)

    return render(request, "redact_profile.html", context)


def complaint(request):
    context = {}
    return render(request, "complaint.html", context)
# Create your views here.
