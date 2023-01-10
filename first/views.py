from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from first.models import DiscreteVotings


def voting_page(request, voting_id):
    context = {}
    if request.method == "POST":
        print(request.POST)
        if request.POST['variant']:
            t = DiscreteVotings.objects.get(id=voting_id)
            if request.POST['variant'] == t.first_option:
                t.first_option_count += 1
            elif request.POST['variant'] == t.second_option:
                t.second_option_count += 1
            t.save()
            return HttpResponseRedirect('/voting/')

    context['VOting'] = get_object_or_404(DiscreteVotings, id=voting_id)
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
