# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from django.core.exceptions import ObjectDoesNotExist
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

# Create your models here.
class BlogManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # check length of first and last name
        if len(postData['first_name']) < 2:
            errors['first_name']= "Field name is too short has to be more than 2 letters"
        if len(postData['last_name']) < 2:
            errors['last_name']= "Field name is too short has to be more than 2 letters"
        # check length of the password
        if len(postData['password']) < 8:
            errors['password']= "Password must be at least 8 characters"
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = ("Invalid email format")
        if not re.match(NAME_REGEX, postData['first_name']):
            errors['first_name'] = ("First name field")
        if not re.match(NAME_REGEX, postData['last_name']):
            errors['last_name'] = ("Last Name name field")
        # check password == password_confirm
        if postData['password'] != postData['cfpassword']:
            errors['password']=("Passwords don't match")
        try:
            Users.objects.get(email = postData['email'])
        except ObjectDoesNotExist:
            pass
        else: 
            errors['email'] = "email is already been used"
        if errors:
            return errors
        else:
            hashed = bcrypt.hashpw(postData['password'].encode('utf8'), bcrypt.gensalt(5))
            print hashed
            Users.objects.create(first_name=postData['first_name'],last_name=postData['last_name'],email=postData['email'], password=hashed)
            return errors

    def login_validator(self, postData):
        errors = {}
        # if not EMAIL_REGEX.match(postData['email']):
        #     errors['email']('Please enter a valid email!')
        if len(postData['email']) < 8:
            errors['email'] = "Email Invaild"
        if len(postData['password']) < 8:
            errors['password'] = "Password Invalid"
        if errors:
            print "FAILING BASIC VALIDATIONS"
            return errors 
        try:
            print "GOT TO THE TRY BLOCK"
            correct_user = Users.objects.get(email = postData['email'])
            print postData['password']
            print correct_user.password
            if not bcrypt.checkpw(postData['password'].encode('utf8'), correct_user.password.encode('utf8')):
                errors['password'] = 'invalid credentials!!!!!!!!'
        except:
            errors['email'] = "No user registered with that email"
        return errors
    
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    cfpassword = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BlogManager()

# class ReviewManager(models.Manager):
#     def validate_review(self, postdata):
#         errors = {}
#         if len(postdata['title']) < 2:
#             errors['title']= "Field name is too short has to be more than 2 letters"
#         if len(postdata['review']) < 1:
#             errors['review'] = "Fields are required"
#         return errors
#         if len(postdata['title']) < 4:
#              errors['title']= 'fields are required'
#         if len(postdata['review']) < 1:
#             errors['title']= 'fields are required'
#         if not "author" in postdata and len(postdata['new_author']) < 3:
#             errors['author']= 'new author names must 3 or more characters'

#         if "author" in postdata and len(postdata['new_author']) > 0 and len(postdata['new_author']) < 3:
#             errors['authors']= 'new author names must 3 or more characters'
#         # if not int(postdata['rating']) > 0 or not (postdata['rating']) <= 5:
#         #     errors['authors'] = 'invalid rating'
#         return errors

#     def create_review(self, clean_data, user_id):
#         # retrive or create author
#         the_author = None
#         if len(clean_data['new_author']) < 1:
#             the_author = Author.objects.get(id=int(clean_data['author']))
#         else:
#             the_author = Author.objects.create(name=clean_data['new_author'])
#         # retirive or create book
#         the_book = None
#         if not Book.objects.filter(title=clean_data['title']):
#             the_book = Book.objects.create(
#                 title=clean_data['title'], author=the_author
#             )
#         else:
#             the_book = Book.objects.get(title=clean_data['title'])
#         # returns a Review object
#         return self.create(
#             review = clean_data['review'],
#             rating = clean_data['rating'],
#             book = the_book,
#             reviewer = Users.objects.get(id=user_id)
#         )
        
# class Author(models.Model):
#     name = models.CharField(max_length=100)

# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     author = models.ForeignKey(Author, related_name="books")

# class Review(models.Model):
#     review = models.TextField()
#     rating = models.IntegerField()
#     book = models.ForeignKey(Book, related_name="reviews")
#     reviewer = models.ForeignKey(Users, related_name="reviews_left")
#     created_at = models.DateTimeField(auto_now_add=True)
#     objects = ReviewManager()
