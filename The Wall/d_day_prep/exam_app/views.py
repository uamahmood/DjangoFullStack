from django.contrib import messages
from django.shortcuts import redirect, render

import bcrypt

from .models import *

# from .models import User, Comment, Message


def index(request):
    return render(request, 'index.html')


def wall(request):
    if 'uuid' not in request.session:
        return redirect('/')
    user_id = request.session['uuid']
    context = {
        'user': User.objects.get(id=user_id),
        'all_messages': Message.objects.all().order_by('-created_at')
    }
    return render(request, 'wall.html', context)


def register(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['register_password']
        hash_browns = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name=request.POST['register_first_name'],
            last_name=request.POST['register_last_name'],
            email=request.POST['register_email'],
            password=hash_browns
        )
        request.session['uuid'] = user.id
        return redirect('/wall')


def logout(request):
    request.session.flush()
    return redirect('/')


def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login = User.objects.get(
            email=request.POST['login_email'])
        request.session['uuid'] = user_to_login.id
        return redirect('/wall')


def messages_create(request):
    print(request.POST)
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        # who posted message?
        user_who_posted = User.objects.get(id=request.session['uuid'])
        # create the message
        Message.objects.create(
            post_message=request.POST['user_message'],
            user_who_post=user_who_posted
        )
    return redirect('/wall')


def comments_create(request):
    print(request.POST)
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        # who posted comment?
        user_obj_who_commented = User.objects.get(id=request.session['uuid'])
        # create the comment
        message_obj = Message.objects.get(id=request.POST['message_id'])
        Comment.objects.create(
            text=request.POST['user_comment'],
            message=message_obj,
            commenter=user_obj_who_commented
        )
    return redirect('/wall')


def messages_delete(request, message_id):
    # How do we delete a message?
    Message.objects.get(id=message_id).delete()

    # message_to_delete = Message.objects.get(id=message_id)
    # message_to_delete.delete()
    return redirect('/wall')


def messages_like(request, message_id):
    # What message are we liking?
    message_to_like = Message.objects.get(id=message_id)
    # Who liked the message?
    user_doing_the_liking = User.objects.get(id=request.session['uuid'])

    # How do you like it?
    message_to_like.users_who_liked.add(user_doing_the_liking)
    return redirect('/wall')


def messages_dislike(request, message_id):
    message_to_like = Message.objects.get(id=message_id)
    user_doing_the_liking = User.objects.get(id=request.session['uuid'])
    message_to_like.users_who_liked.remove(user_doing_the_liking)
    return redirect('/wall')