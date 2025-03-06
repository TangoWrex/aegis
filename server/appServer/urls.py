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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from search.views import search_view
from django.db.models import Q
from search.models import Document, DeviceLocation, APIKey, ChatMessage
import json
import os

def index(request):
    devices = []
    return render(request, 'index.html', {'devices': devices})

def console(request):
    chat_query = request.GET.get('chat_q', '').strip()
    chat_results = []
    if chat_query:
        chat_results = ChatMessage.objects.filter(message__icontains=chat_query).order_by('-timestamp')[:10]
    
    connected_devices = DeviceLocation.objects.values('device_id').distinct()
    devices = [device['device_id'] for device in connected_devices]
    
    return render(request, 'map.html', {
        'chat_query': chat_query,
        'chat_results': [{'device_id': msg.device_id, 'message': msg.message} for msg in chat_results],
        'devices': devices,
        'api_key': os.getenv("AEGIS_API_KEY")  # Pass API key to template
    })

def about(request):
    return render(request, 'about.html')

@csrf_exempt
def device_locations(request):
    api_key = request.headers.get('X-API-Key')
    if not api_key or not APIKey.objects.filter(key=api_key).exists():
        return JsonResponse({"error": "Invalid or missing API key"}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            device_id = data.get("device_id")
            latitude = float(data.get("latitude", 0))
            longitude = float(data.get("longitude", 0))
            DeviceLocation.objects.create(
                device_id=device_id,
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({"status": "success"}, status=201)
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            return JsonResponse({"error": str(e)}, status=400)
    elif request.method == "GET":
        locations = DeviceLocation.objects.all()
        data = [{"lat": loc.latitude, "lon": loc.longitude, "device_id": loc.device_id} for loc in locations]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def chat_messages(request):
    api_key = request.headers.get('X-API-Key')
    if not api_key or not APIKey.objects.filter(key=api_key).exists():
        return JsonResponse({"error": "Invalid or missing API key"}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            device_id = data.get("device_id")
            message = data.get("message")
            ChatMessage.objects.create(device_id=device_id, message=message)
            return JsonResponse({"status": "success"}, status=201)
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

urlpatterns = [
    path('', index, name='index'),
    path('console', console, name='console'),
    path('about', about, name='about'),
    path('search', search_view, name='search'),
    path('api/locations/', device_locations, name='device_locations'),
    path('api/chat/', chat_messages, name='chat_messages'),
]