# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import *
from models import Books, Authors, Reviews
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.template import Template, Context

# Create your views here.
def new_book(request):
    if request.method == "POST":
        errors = Books.objects.validateBooks(request.POST)
        if len(errors):
            for key, error in errors.iteritems():
                print error
        return redirect('/books')
    else:
        context = {
            'authors': Authors.objects.all()
        }
        return render(request, 'books/new_book', context)

def displaybook(request):
    return render(request, 'displaybook.html')
   