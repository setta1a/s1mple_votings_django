import datetime

from django.shortcuts import render, get_object_or_404

from first.models import Voting, VoteVariant, VoteFact


def voting_page(request, voting_id):
    context = {}
    if request.method == "POST":
        if request.POST.get('variant_id') and request.user.is_authenticated and not VoteFact.objects.filter(author = request.user):
            record = VoteFact(variant_id=request.POST['variant_id'],
                              created_at = datetime.datetime.now(),
                              author=request.user)
            record.save()

    context['voting'] = get_object_or_404(Voting, id=voting_id)
    context["voting_variants"] = VoteVariant.objects.filter(voting = voting_id)
    return render(request, 'voting.html', context)


def list_of_votings_page(request):
    context = {}
    return render(request, 'list_of_votings.html', context)


def authorization_page(request):
    context = {}
    return render(request, 'authorization.html', context)


def index_page(request):
    context = {}
    return render(request, 'index.html', context)

# Create your views here.
