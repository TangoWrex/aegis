from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    file_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.title)
        

class DeviceLocation(models.Model):
    device_id = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class APIKey(models.Model):
    key = models.CharField(max_length=40, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
    
class ChatMessage(models.Model):
    device_id = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_id}: {self.message}"