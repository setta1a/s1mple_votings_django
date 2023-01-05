from django.shortcuts import render

def voting_page(request):
    context = {}
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
