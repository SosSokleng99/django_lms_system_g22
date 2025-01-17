from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def aboutUs(request):
    return render(request, 'about-us.html')