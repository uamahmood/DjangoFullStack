from django.shortcuts import render, HttpResponse, redirect
from .models import Show
from datetime import datetime, time, timezone
from time import gmtime, strftime
from django.contrib import messages

def AddNewShow(request): 
    context = {
        'shows': Show.objects.all()
    }
    return render(request, 'srts_app/AddNewShow.html', context)

def CreateNewShow(request): 
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shows/new')
    else:
        show = Show.objects.create(title=request.POST['title'], network=request.POST['network'], release_date=request.POST['release_date'], description=request.POST['description'])
        messages.success(request, "Show successfully created")
        return redirect(f'/shows/{show.id}')

def TvShow(request, id): 
    context = {
        'show': Show.objects.get(id=id)
    }
    return render(request, 'srts_app/TVShow.html', context)

def AllShows(request): 
    context = {
        'shows': Show.objects.all()
    }
    return render(request, 'srts_app/AllShows.html', context)

def EditShow(request, id):
    context = {
        'show': Show.objects.get(id=id)
    }
    return render(request, 'srts_app/EditShow.html', context)

def UpdateShow(request, id):
    print("Request", request)
    print(request.POST)
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/shows/{id}/edit')
    else:
        show = Show.objects.get(id=id)
        show.title = request.POST['title']
        show.network = request.POST['network']
        show.release_date = request.POST['release_date']
        show.description = request.POST['description']
        show.save()
        return redirect(f'/shows/{id}')

def DeleteShow(request, id):
    show = Show.objects.get(id=id)
    show.delete()
    return redirect('/shows')

def index(request):
    return redirect('/shows')