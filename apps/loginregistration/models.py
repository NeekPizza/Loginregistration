from __future__ import unicode_literals
from django.contrib import messages
import bcrypt
from django.db import models
import re

# Create your models here.

class UsersManager(models.Manager):
    def registration(self,form):
        ncheck = re.compile(r'[a-z A-Z]')
        echeck = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pwcheck = re.compile(r'.*\d.*[A-Z].*|.*[A-Z].*\d.*')
        hashed=bcrypt.hashpw(form['password'].encode('utf-8'),bcrypt.gensalt())
        errors=[]
        if len(form['first_name'])<2:
            errors.append('Name too short')
        if not ncheck.match(form['first_name']):
            errors.append('Name invalid')
        if len(form['last_name'])<2:
            errors.append('Last name too short')
        if not ncheck.match(form['first_name']):
            errors.append('Last name invalid')
        if not echeck.match(form['email']):
            errors.append('Invalid email')
        if not pwcheck.match(form['password']):
            errors.append('Invalid password')
        if not form['password'] == form['confirm_password']:
            errors.append('Passwords do not match')
        if len(form['password'])<8:
            errors.append('Password too short')
        if len(errors)>0:
            return (False,errors)
        else:
            user=Users.objects.create(first_name=form['first_name'],last_name=form['last_name'],email=form['email'],password=hashed)
            return (True,user)

    def login(self,form):
        errors=[]
        user=Users.objects.filter(email=form['email'])


        if not user:
            errors.append('Email does not match records')
        elif not bcrypt.hashpw(form['password'].encode('utf-8'),user[0].password.encode('utf-8'))==user[0].password:
            errors.append('Password does not match email')
        if len(errors)>0:
            return (False,errors)
        else:
            return (True,user)


class Users(models.Model):
    first_name=models.CharField(max_length=21)
    last_name=models.CharField(max_length=21)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

    objects=UsersManager()
