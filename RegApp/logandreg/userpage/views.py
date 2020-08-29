from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt


def index(request):
    return render (request, "index.html")
    
def success(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uuid'])
    }
    return render (request, "success.html", context)

def register(request):
    print(request.POST)
    # TODO
    print('registering a user')
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        print('registering a user')
        password = request.POST['register_password']
        hash_browns = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
        print('password: ', password)  
        print('hash_browns: ', hash_browns)      
        user = User.objects.create(
        alias=request.POST['register_alias'], 
        email=request.POST['register_email'],
        password=hash_browns) 
        request.session['uuid'] = user.id
        return redirect('/success')

def login(request):
    print(request.POST)
    # TODO  
    print('logging in a user')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login = User.objects.get(
            email=request.POST['login_email'])
        print ('user_to_login: ', user_to_login)
        request.session['uuid'] = user_to_login.id
        return redirect('/success')
    
def logout(request):
    request.session.flush()
    return redirect('/')