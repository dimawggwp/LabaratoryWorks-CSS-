from django.urls import path
from django.shortcuts import render

def home(request):
    return render(request, 'todesign.html')

urlpatterns = [
    path('', home),
]