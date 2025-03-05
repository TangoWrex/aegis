"""
URL configuration for appServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.shortcuts import render
from search.views import search_view
from django.db.models import Q
from search.models import Document


def index(request):
    devices = []  # Placeholder - add real device data later
    return render(request, 'index.html', {'devices': devices})

def console(request):
    chat_query = request.GET.get('chat_q', '').strip()
    chat_results = []
    if chat_query:
        chat_results = [f"Searched for: {chat_query}"]
    return render(request, 'map.html', {
        'chat_query': chat_query,
        'chat_results': chat_results
    })

def about(request):
    return render(request, 'about.html')

urlpatterns = [
    path('', index, name='index'),
    path('console', console, name='console'),
    path('about', about, name='about'),
    path('search', search_view, name='search'),
]