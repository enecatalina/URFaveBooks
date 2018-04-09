# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import *
from models import Books, Authors, Reviews
from ..logreg_app.models import *
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, reverse


# Create your views here.
def success(request):
    # if request.session['user_id'] == None:
    #     return redirect(reverse('Users:index'))
    print "Books/Success Page "
    context = {
        'user': Users.objects.all(),
        'current_user': Users.objects.get(id=request.session['user_id']),
        'books': Books.objects.all(),
        'reviews' : Reviews.objects.last(),
        }
    return render(request, "success.html", context)

def create(request):
    current_user = request.session['user_id']
    find_authors = Authors.objects.all()
    # if request.session['user_id'] == None:
    #     return redirec==t(reverse('Users:index'))
    if request.method == "POST":
        errors = Books.objects.validateBooks(request.POST, request.FILES , current_user)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('Books:Create'))
    else:
        context = {
            'authors' : find_authors
        }
    return render(request, 'create.html', {'authors': find_authors})

def displaybook(request):
    return render(request, 'displaybook.html')

def logout(request):
    request.session.clear()
    return redirect('/')