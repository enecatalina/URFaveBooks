# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..logreg_app.models import Users

# Create your models here.
class BooksValidator (models.Manager):
    def validateBooks(self,postDate):
        errors = {}
        new_author = False
        if len(postDate['title']) < 2:
            errors['title'] = "Title must have more then 2 characters" 
        if len(postDate['author']) == 'None' and postDate['inputed_author'] == 'name':
            errors['author'] = 'An author must be selected or added before submiting form'
        if postDate['author'] != 'None' and postDate['inputed_author'] != 'name':
            errors['author'] = 'You cannot select an author and try to add a new one at the same time'
        try:
            #is the author already in the database?
            Books.objects.get(author=postDate['inputed_author'])
            #error message
            errors['author'] = 'You cannot select an author and try to add a new one at the same time'
        except Exception:
            if postDate['inputed_author'] != 'name':
                new_author = True
        
        if postDate['review'] < 10:
            errors['review'] = 'Your review needs to be more than ten characters long before submitting'
        if errors:
            return (errors)

        # What author selection was used?
        #IF (TRUE) there was a NEW author selected 
        if new_author:
            #what is the name of the new author?
            input_created_author = postDate['inputed_author']
            print input_created_author
            #create the author and store in VAR
            new_author = Authors.objects.create(author_name = input_created_author)
            #Put the new author in a new VAR to use when CREATING the BOOK
            author_for_book_created = new_author
        else:
            #IF FALSE 
            #take the name of the SELECTED author
            selected_author = postDate['selected_author']
            print  selected_author 
            #find the name of the selected author
            author_for_book_created = Authors.objects.get(name = selected_author)
            
        #Creating a new book
        title = postDate['title']
        user_id = postDate['user_id']
        new_book_created = Books.objects.create(title=title, author=author_for_book_created, user_id=user_id)
        print new_book_created

        #Create the review
        text = postDate['review']
        rating = postDate['rating']
        reviewer = postDate['user_id']
        try:
            print "Trying to create book review"
            book_id = postDate['book_id']
            book_search = Books.objects.get(id=book_id)
        except Exception:
            errors['book']= 'Book is not in the database'
        if errors:
            return errors
        Reviews.objects.create(text=text, rating=rating, reviewer=reviewer, book = new_book_created)
        return errors

class Authors(models.Model):
    author_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BooksValidator()

class Books(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(Authors, related_name='authors')
    user = models.ForeignKey(Users, related_name = "who_created_book", null=True)
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




            