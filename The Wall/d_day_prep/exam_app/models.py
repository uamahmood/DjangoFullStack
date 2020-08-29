import re  # the regex module

from django.db import models

import bcrypt


class UserManager(models.Manager):
    def register_validator(self, postal_dataz):
        errors = {}

        if len(postal_dataz['register_first_name']) < 2:
            errors['register_first_name'] = "Your first name needs to be at least 2 characters"

        if len(postal_dataz['register_last_name']) < 2:
            errors['register_last_name'] = "Your last name needs to be at least 2 characters"

        # email format
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # test whether a field matches the pattern
        if EMAIL_REGEX.match(postal_dataz['register_email']) == None:
            errors['register_email'] = "Invalid email address!"

        # password confirm
        if postal_dataz['register_password'] != postal_dataz['register_password_confirm']:
            errors['register_password'] = 'Password does not match'

        # password length
        if len(postal_dataz['register_password']) <= 7:
            errors['register_password_confirm'] = 'Password is too short, must be at least 8 characters'

        # uniqueness
        return errors

    def login_validator(self, postal_dataz):
        errors = {}

        user_list_to_login = User.objects.filter(
            email=postal_dataz['login_email'])
        if len(user_list_to_login) == 0:
            errors['login_email'] = 'There was a problem email'
        else:
            if not bcrypt.checkpw(postal_dataz['login_password'].encode(), user_list_to_login[0].password.encode()):
                errors['login_password'] = 'There was a problem pw'

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    # messages 1 -> Many
    # comments 1 -> Many
    messages_liked = models.ManyToManyField('Message', related_name='users_who_liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class MessageManager(models.Manager):
    def message_validator(self, postal_dataz):
        errors = {}
        if len(postal_dataz['user_message']) < 2:
            errors['user_message'] = "Your message needs to be at least 2 characters"

        return errors


class Message(models.Model):
    post_message = models.CharField(max_length=255)
    user_who_post = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE)
    # comments 1 -> Many
    # users_who_liked Many <-> Many
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class CommentManager(models.Manager):
    def comment_validator(self, postal_dataz):
        errors = {}
        if len(postal_dataz['user_comment']) < 2:
            errors['user_comment'] = "Your comment needs to be at least 2 characters"

        return errors

class Comment(models.Model):
    text = models.CharField(max_length=255)
    message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()