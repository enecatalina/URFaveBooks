from django.conf.urls import url, include
from django.contrib import admin
from . import views           # This line is new!

urlpatterns = [
    # url(r'^$', views.index, name = 'index'),
     url(r'^(?P<number>\d+)$', views.displaybook, name='displaybook'),
    # url(r'^success$', views.success, name = "success"),
    url(r'^new_book$', views.new_book, name = "new_book"),
    # url(r'^login$', views.login, name = "login"),
    # url(r'^logout$', views.logout, name = "logout"),
    # url(r'^user/(?P<user_id>\d+)$', views.show)
]