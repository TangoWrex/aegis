# server/appserver/urls.py
"""
URL configuration for appServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from datetime import datetime

def index(request):
    devices = []
    return render(request, 'index.html', {'devices': devices})

def console(request):
    chat_results = ChatMessage.objects.all().order_by('-timestamp')[:50]
    
    connected_devices = DeviceLocation.objects.values('device_id').distinct()
    devices_data = []
    for device in connected_devices:
        device_id = device['device_id']
        latest_location = DeviceLocation.objects.filter(device_id=device_id).order_by('-timestamp').first()
        if latest_location:
            last_checkin = latest_location.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            last_location = f"({latest_location.latitude}, {latest_location.longitude})"
            device_type = 'user' if device_id == 'console_user' else 'endpoint'
            devices_data.append({
                'device_id': device_id,
                'last_checkin': last_checkin,
                'last_location': last_location,
                'type': device_type
            })

    return render(request, 'map.html', {
        'chat_results': [{'device_id': msg.device_id, 'message': msg.message, 'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for msg in chat_results],
        'devices': devices_data,
        'api_key': os.getenv("AEGIS_API_KEY")
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
    elif request.method == "GET":
        messages = ChatMessage.objects.all().order_by('-timestamp')[:50]
        data = [{"device_id": msg.device_id, "message": msg.message, "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def clear_chat(request):
    api_key = request.headers.get('X-API-Key')
    if not api_key or not APIKey.objects.filter(key=api_key).exists():
        return JsonResponse({"error": "Invalid or missing API key"}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            device_id = data.get("device_id")
            if device_id != 'console_user':
                return JsonResponse({"error": "Only console_user can clear the chat"}, status=403)
            ChatMessage.objects.all().delete()
            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def documents(request):
    api_key = request.headers.get('X-API-Key')
    if not api_key or not APIKey.objects.filter(key=api_key).exists():
        return JsonResponse({"error": "Invalid or missing API key"}, status=403)

    if request.method == "GET":
        docs = Document.objects.all()
        data = [{"title": doc.title, "content": doc.content, "file_path": doc.file_path} for doc in docs]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def packet_handler(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        packet = json.loads(request.body)
        packet_type = packet.get("type")
        device_id = packet.get("device_id")
        api_key = packet.get("api_key")
        data = packet.get("data")
        timestamp = packet.get("timestamp", datetime.utcnow().isoformat() + "Z")
        
        if not api_key or not APIKey.objects.filter(key=api_key).exists():
            return JsonResponse({"error": "Invalid or missing API key"}, status=403)
        
        if packet_type == "gps":
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            if latitude is None or longitude is None:
                return JsonResponse({"error": "Missing GPS data"}, status=400)
            DeviceLocation.objects.create(
                device_id=device_id,
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp
            )
        elif packet_type == "chat":
            message = data.get("message")
            if not message:
                return JsonResponse({"error": "Missing chat message"}, status=400)
            ChatMessage.objects.create(
                device_id=device_id,
                message=message,
                timestamp=timestamp
            )
        else:
            return JsonResponse({"error": "Invalid packet type"}, status=400)
        
        return JsonResponse({"status": "success"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

urlpatterns = [
    path('', index, name='index'),
    path('console', console, name='console'),
    path('about', about, name='about'),
    path('search', search_view, name='search'),
    path('api/locations/', device_locations, name='device_locations'),
    path('api/chat/', chat_messages, name='chat_messages'),
    path('api/packet/', packet_handler, name='packet_handler'),
    path('api/clear_chat/', clear_chat, name='clear_chat'),
    path('api/documents/', documents, name='documents'),
]