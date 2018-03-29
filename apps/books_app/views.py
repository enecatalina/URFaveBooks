# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import *
from models import Books, Authors, Reviews
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, reverse


# Create your views here.
def success(request):
    print "show page working"
    context = {
        'user': Users.objects.all(),
        'current_user': Users.objects.get(id=request.session['user_id']),
        'books': Books.objects.all()
        }
    return render(request, "success.html", context)

def create(request):
    if request.method == "POST":
        errors = Books.objects.validateBooks(request.POST)
        if len(errors):
            for key, error in errors.iteritems():
                print error
        return redirect('/books/home.html')
    else:
        context = {
            'authors' : Authors.objects.all()
        }
    return render(request, 'create.html', context)

def displaybook(request):

    return render(request, 'displaybook.html')

   