# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import re
from django.core.exceptions import ObjectDoesNotExist
from ..logreg_app.models import Users
from django.core.files import File

# Create your models here.
class BooksValidator (models.Manager):
    def validateBooks(self, postDate, postFILES, current_user):
        errors = {}
        new_author = False
        if postDate['rating'] == 'selected':
            errors["rating"] = "Please choose a rating"
        # if (int(postDate['rating']) < 1 ) | (int(postDate['rating']) > 5):
        #     errors["rating"] = "Rating should be between 0 and 5"
        if len(postDate['title']) < 3:
            errors['title'] = "Title must have more then 2 characters" 
        if len(postDate['review']) < 10:
            errors['review'] = 'Your review needs to be more than 10 characters long before submitting'
        if postDate['selected_author'] == 'selected_author' and postDate['inputed_author'] == 'author_name':
            errors['selected_author'] = 'An author must be selected or added before submiting form'
        # if postDate['selected_author'] != 'selected_author' and postDate['inputed_author'] != 'author_name':
        #     errors['selected_author'] = 'You cannot try to add an author and create one at the same time'
        try:
            #is the author already in the database?
            Authors.objects.get(author_name = postDate['inputed_author'])
            errors['inputed_author'] = 'This author is already been created'
        except Exception:
            if postDate['inputed_author'] != 'author_name':    
                new_author = True
        try:
            Books.objects.get(title=postDate['title'])
            errors['title'] = "Book is already created"
        except Exception:
           if postDate['title'] != 'title':
                print errors
        if errors:
            return (errors)

        # What author selection was used?
        #IF (TRUE) there was a NEW author selected 
        if new_author:
            #what is the name of the new author?
            input_created_author = postDate['inputed_author']
            print input_created_author 
            print  "Created Author^^^^^^"
            #create the author and store in VAR
            new_author = Authors.objects.create(author_name = input_created_author)
            #Put the new author in a new VAR to use when CREATING the BOOK
            author_for_book_created = new_author
        else:
            #IF FALSE 
            #take the name of the SELECTED author
            selected_author = postDate['selected_author']
            print selected_author
            print  "Selected Author^^^^^^"
            #find the name of the selected author
            author_for_book_created = Authors.objects.get(author_name = selected_author)
        
          #Try grabbing an image if it was uploaded
        try:
            book_covers = postFILES['book_covers']
            print book_covers
        except:
            book_covers = ''
            print 'No image'

        #Creating a new book
        title = postDate['title']
        user_id = postDate['user_id']
        book_covers = book_covers
        new_book_created = Books.objects.create(title=title, author=author_for_book_created, user_id=user_id , book_covers=book_covers)
        print new_book_created

        #Create the review
        print "IN --> create REVIEW"
        text = postDate['review']
        rating = postDate['rating']
        reviewer = postDate['user_id']
        book_review = Reviews.objects.create(text=text, rating=rating, reviewer_id=reviewer, book=new_book_created)
        # print book_review
        if errors:
            return errors

class Authors(models.Model):
    author_name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BooksValidator()

class Books(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(Authors, related_name='authors')
    user = models.ForeignKey(Users, related_name = "who_created_book", null=True)
    book_covers = models.ImageField(upload_to="'uploads/%Y/%m'", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BooksValidator()

    def __str__(self):
        return "Title: " + self.title

    def __repr__(self):
        return "<Books object: title: {}, author: {} >".format(self.title, self.author)

class Reviews(models.Model):
    text = models.TextField(default = "N/A")
    rating = models.IntegerField()
    book = models.ForeignKey(Books, related_name = "book_reviewed")
    reviewer = models.ForeignKey(Users, related_name = "who_reviewed_book")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "Reviews: " + self.reviewer

    def __repr__(self):
        return "<Reviews Object: text: {}, rating: {}, book: {}, reviewer: {}>".format(self.text, self.rating, self.reviewer, self.book)




            