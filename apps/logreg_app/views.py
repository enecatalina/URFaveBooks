# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import *
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def create(request):
    # if request.session['user_id'] == None:
    #     return redirect(reverse('Users:index'))
    errors = Users.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        messages.success(request,"You have logged in!")
        current_user = Users.objects.get(email = request.POST['email'])
        request.session['user_id'] = current_user.id
        print "user was created"
        return redirect('books/success')
    print "user was able to create profile"


def login(request):
    # if request.session['user_id'] == None:
    #     return redirect(reverse('Users:index'))
    print "IN --> login"
    errors = Users.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error)            
            return redirect('/')
    else:
        current_user = Users.objects.get(email=request.POST['email'])
        request.session['user_id']= current_user.id
        return redirect('books/success')
    print "user was able to login"

def logout(request):
    request.session.clear()
    return redirect('/')