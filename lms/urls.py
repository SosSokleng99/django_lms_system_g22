from django.urls import path
from . import views

#To defined URL for app
urlpatterns = [
    path('', views.home, name="home"), #Defualt

    path('about-us', views.aboutUs, name='about-us')
]