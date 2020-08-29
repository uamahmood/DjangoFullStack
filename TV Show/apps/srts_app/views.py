from django.shortcuts import render, HttpResponse, redirect
from .models import Show
from datetime import datetime, time, timezone
from time import gmtime, strftime

# Create your views here.
# *********************************************
# 1. # GET /shows/new ------ 'show' was 'shows'
def AddNewShow(request): # GET /shows/new 
    context = {
        'shows': Show.objects.all()
    }
    return render(request, 'srts_app/AddNewShow.html', context)
# *********************************************
#2. # POST /shows/create
def CreateNewShow(request): # POST /shows/create
    show = Show.objects.create(title=request.POST['title'], network=request.POST['network'], release_date=request.POST['release_date'], description=request.POST['description'])
    return redirect(f'/shows/{show.id}')
# *********************************************
# 3. GET shows/id
def TvShow(request, id): # GET /shows/<id>
    context = {
        'show': Show.objects.get(id=id)
    }
    return render(request, 'srts_app/TVShow.html', context)
# *********************************************
# 4 GET /shows ------ 'show' was 'shows'
def AllShows(request): # GET /shows
    context = {
        'shows': Show.objects.all()
    }
    return render(request, 'srts_app/AllShows.html', context)
# *********************************************
# 5 GET /shows/<id>
def EditShow(request, id):
    context = {
        'show': Show.objects.get(id=id)
    }
    return render(request, 'srts_app/EditShow.html', context)
# *********************************************
# 6 POST shows/<id>/update
def UpdateShow(request, id):
    show = Show.objects.get(id=id)
    show.title = request.POST['title']
    show.network = request.POST['network']
    show.release_date = request.POST['release_date']
    show.description = request.POST['description']
    show.save()
    return redirect(f'/shows/{id}')
# *********************************************
# 7 POST shows/<id>/destroy
def DeleteShow(request, id):
    show = Show.objects.get(id=id)
    show.delete()
    return redirect('/shows')
# *********************************************
# 8 POST /shows Root Rout redirects to /shows
def index(request):
    return redirect('/shows')