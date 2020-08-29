import re
import bcrypt
from django.db import models


class UserManager(models.Manager):
    def register_validator(self, postal_dataz):
        errors = {}
        # TODO
        # alias < 3
        if len(postal_dataz['register_alias']) < 3:
            errors['register_alias'] = "Your alias needs to be at least 3 characters"
        # email format
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(postal_dataz['register_email']):    # test whether a field matches the pattern            
            errors['register_email'] = "Invalid email address!"
        # password confirm
        if postal_dataz['register_password'] != postal_dataz['register_password_confirm']:
            errors['register_password'] = 'Password does not match'

        if len(postal_dataz['register_password']) < 9:
            errors['register_password_confirm'] = 'Password is too short'
        # 
        # uniqueness
        return errors

    def login_validator(self, postal_dataz):
        errors = {}
        # TODO
        user_list_to_login = User.objects.filter(email=postal_dataz
        ['login_email'])
        if len(user_list_to_login)==0:
            print('we did  not find a user')
            #errors['login_email'] = 'Email not found'
            errors['login_email'] = 'There was a problem email'
        else:
            if not bcrypt.checkpw(postal_dataz['login_password'].encode(), 
            user_list_to_login[0].password.encode()):
                print('Password does not match')
                errors['login_password'] = 'There was a problem with the password'
        return errors


class User(models.Model):
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()