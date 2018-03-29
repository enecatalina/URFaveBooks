from django.conf.urls import url, include
from django.contrib import admin
from . import views           # This line is new!

urlpatterns = [
    url(r'^success$', views.success, name = "Success"), #HomePage
    url(r'^create$', views.create, name = "Create"), #Creating the book 
    url(r'^(?P<number>\d+)$', views.displaybook, name='Displaybook'), # Display the book
    # url(r'^logout$', views.logout, name = "logout"),
    # url(r'^user/(?P<user_id>\d+)$', views.show)
]