from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    file_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.title)
        