from django.http import HttpResponseRedirect
from django.shortcuts import render

from first.models import DiscreteVotings


def voting_page(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
        if request.POST['variant']:
            t = DiscreteVotings.objects.all()[0]
            if request.POST['variant'] == t.first_option:
                t.first_option_count += 1
            elif request.POST['variant'] == t.second_option:
                t.second_option_count += 1
            t.save()
            return HttpResponseRedirect('/voting/')

    context['VOting'] = DiscreteVotings.objects.all()[0]
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
