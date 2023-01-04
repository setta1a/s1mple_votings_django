from django.shortcuts import render

def voting_page(request):
    context = {}
    return render(request, 'voting.html', context)


def list_of_votings_page(request):
    context = {}
    return render(request, 'list_of_votings.html', context)

# Create your views here.
