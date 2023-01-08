from django.shortcuts import render

from first.models import DiscreteVotingZ


def voting_page(request):
    context = {}
    if request.method == "POST":
        print(request.POST)


    context['VOting'] = DiscreteVotingZ.objects.all()[0]
    return render(request, 'voting.html', context)


def list_of_votings_page(request):
    context = {}
    return render(request, 'list_of_votings.html', context)


def authoriZation_page(request):
    context = {}
    return render(request, 'authoriZation.html', context)


def index_page(request):
    context = {}
    return render(request, 'index.html', context)

# Create your views here.
