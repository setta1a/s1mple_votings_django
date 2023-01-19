import datetime

from django.shortcuts import render, get_object_or_404

from first.models import Voting, VoteVariant, VoteFact


def voting_page(request, voting_id):
    context = {}
    context["pagetitle"] = "Голосование"
    context["pageheader"] = "Было два стула"
    context['voting'] = get_object_or_404(Voting, id=voting_id)
    context["voting_variants"] = VoteVariant.objects.filter(voting=voting_id)
    if request.method == "POST":
        is_voted = False
        for votefact in VoteFact.objects.filter(author = request.user):
            if VoteVariant.objects.filter(id=votefact.variant_id).filter(voting_id=voting_id).count() != 0:
                is_voted = True
                context["is_voted"] = is_voted
                break

        if request.user.is_authenticated and not is_voted:
            record = VoteFact(variant_id=request.POST['variant_id'],
                              created_at = datetime.datetime.now(),
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
    return render(request, 'add_voting.html', context)

# Create your views here.
