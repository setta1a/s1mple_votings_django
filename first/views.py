import datetime

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404

from first.models import Voting, VoteVariant, VoteFact


def voting_page(request, voting_id):
    context = {}
    context["all_votes_count"] = 0
    context["pagetitle"] = "Голосование"
    context["pageheader"] = "Было два стула"
    context['voting'] = get_object_or_404(Voting, id=voting_id)
    context["voting_variants"] = VoteVariant.objects.filter(voting=voting_id)
    for el in VoteVariant.objects.filter(voting=voting_id):
        context["all_votes_count"] += el.votes_count
    if request.method == "POST":
        is_voted = False
        for votefact in VoteFact.objects.filter(author=request.user):
            if VoteVariant.objects.filter(id=votefact.variant_id).filter(voting_id=voting_id).count() != 0:
                is_voted = True
                context["is_voted"] = is_voted
                break

        if request.user.is_authenticated and not is_voted:
            record = VoteFact(variant_id=request.POST['variant_id'],
                              created_at=datetime.datetime.now(),
                              author=request.user)
            record.save()

    return render(request, 'voting.html', context)


def list_of_votings_page(request):
    context = {}
    context["pagetitle"] = "List of votings"
    context["pageheader"] = "Все голосования"
    context["votings_list"] = Voting.objects.all()
    return render(request, 'list_of_votings.html', context)


def index_page(request):
    context = {}
    context["pagetitle"] = "Index page"
    context["pageheader"] = "Главная"
    return render(request, 'index.html', context)


def add_voting(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
        if int(request.POST['voting_type']) and request.POST['theme'] and request.POST.get(
                "variants") and request.user.is_authenticated and request.POST['description']:
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

    return render(request, 'add_voting.html', context)


def registration(request):
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
    context = {}
    context['voting'] = get_object_or_404(Voting, id=voting_id)
    context['variants'] = VoteVariant.objects.filter(voting_id = voting_id)
    if request.method == "POST":
        print(request.POST)
        if int(request.POST['voting_type']) and request.POST['theme'] and request.POST.get(
                "variants") and request.user.is_authenticated and request.POST['description']:
            voting_tochange = Voting.objects.get(id=voting_id)
            voting_tochange.voting_type = int(request.POST['voting_type'])
            voting_tochange.name = request.POST['theme']
            voting_tochange.description = request.POST['description']
            voting_tochange.save()

            VoteVariant.objects.filter(voting_id = voting_id).delete()
            for variant in request.POST.getlist("variants"):
                new_variant = VoteVariant(
                    description=variant,
                    voting=voting_tochange,
                )
                new_variant.save()
    return render(request, 'redact_voting.html', context)

# Create your views here.
