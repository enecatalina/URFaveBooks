# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import *
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse

# Create your views here.
def newbook(request):
    
    return render(request, "newbook.html")
    # if request.method == 'POST':
    #     errors = Book.objects.book_validator(request.POST)
    #     if len(errors):
    #         for key, error in errors.iteritems():
    #             print error
    #         return redirect('books_app/newbook.html')
    #     else:
    #         context = {
    #             'all_authors' : Author.objects.all()
    #         }
    #         return render(request,'logreg_app/success.html',context)
    #     the_book = Book.objects.get(id=id_book)
    #     title = request.POST['title'],
    #     author = the_book.author.id,
    #     rating = request.POST['rating']
    #     review = request.POST['review']
    #     new_author = ''
    #     Review.objects.create(tite=title,rating=rating,review=review)   
    #     return render(request, "newbook.html") 