# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class BooksValidator (models.Manager):
    def book_validator(self,postDate):
        errors = {}
        new_author = False

        if len(postDate['title']) < 1: 
            errors['title'] = 'The title of the book most be entered'
        if postDate['author'] == 'None' and postDate['new_input_author'] == 'name':
            errors['author'] = 'An author must be selected or added'
        if postDate['author'] != 'None' and postDate['new_input_author'] != 'name':
            errors['author'] = 'You are not able to select a author and try to add a new one at the same time'
        try:
            #if the author in the database?
            Author.objects.get(name=postDate['new_input_author'])
            #if yes:
            errors['author'] = 'Author is already in our system'
        except Exception:
            if postDate['new_input_author'] != 'name':
                new_author = True
        
        if postDate['review'] < 10:
            errors['review'] = 'Your book review needs to be more than 10 characters'
        if errors:
            return (errors)
        
        #What author selection was used?
        #IF (TRUE) there was a NEW author selected 
        if new_author:
            #what is the name of the new author?
            input_created_author = postDate['new_input_author']
            print input_created_author
            #create the author and store in VAR
            new_author = Author.objects.create(name = input_created_author)
            #Put the new author in a new VAR to use when CREATING the BOOK
            author_for_book_created = new_author
        else:
            #IF FALSE 
            #take the name of the SELECTED author
            selected_author = postDate['selected_author']
            print  selected_author 
            #find the name of the selected author
            author_for_book_created = Author.objects.get(name = selected_author)
            
        #Creating a new book
        created_title = postDate['title']
        new_book_created = Book.objects.create(title=created_title, author=author_for_book_created)
        print new_book_created

    def review_validator(self,postDate):
        errors = {}
        if len(postDate['review']) < 15:
            errors['review'] = 'Review must be at least 15 characters long'

        input_review = postDate['review']
        input_rating = postDate['rating']
        user_name = postDate['user_name']
        id_user = postDate['id_user']
        #try to retrieve the book this review is for
        try:
            id_book = postDate['id_book']
            find_book = Book.objects.get(id=id_book)
        except Exception:
            errors['book'] = 'Could not find book'
        if errors:
            return errors
        Review.objects.create(content=input_review, rating=input_rating,
                                commentor=user_name, commentor_id=id_user, book=find_book)
        return (errors)


class Author(models.Model):
    name = models.CharField(max_length=100)
    objects = BooksValidator()

    # def __str__(self):
    #     return "Name: " + self.name

    # def __repr__(self):
    #     return "<Authors object: name: {}>".format(self.name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BooksValidator()

    # def __str__(self):
    #     return "Title: " + self.title

    # def __repr__(self):
    #     return "<Books object: title: {}, author: {} >".format(self.title, self.author)

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    commentor = models.IntegerField(max_length=20)
    commentor_id = models.IntegerField()
    book = models.ForeignKey(Book, related_name="reviews")
    reviewer = models.ForeignKey(Book, related_name="user_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    objects = BooksValidator()


            