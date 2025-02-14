"""
URL configuration for lms_system_G22 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('lms/', include("lms.urls")),

    #URL for User Authentication
    path('accounts/', include('django.contrib.auth.urls')),

]


#Redirect to Based URL of LMS e.g. http://127.0,1.8000/lms/
from django.views.generic import RedirectView

urlpatterns += [
    path("", RedirectView.as_view(url="/lms/", permanent = True))
]