"""
This script populates the Document model in the Django database with files from the 
static/docs/ directory.
It reads each file’s content and creates a Document entry if it doesn’t already exist, 
linking to the file path.
"""

import os
import django
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appServer.settings")

# Configure Django settings before importing models
django.setup()

# Now safe to import models
from search.models import Document

def populate_documents():
    docs_dir = os.path.join(settings.STATICFILES_DIRS[0], 'docs')
    for filename in os.listdir(docs_dir):
        if os.path.isfile(os.path.join(docs_dir, filename)):
            # Check if already in DB
            if not Document.objects.filter(title=filename).exists():
                with open(os.path.join(docs_dir, filename), 'r') as f:
                    content = f.read()
                Document.objects.create(
                    title=filename,
                    content=content[:1000],  # Truncate if too long, adjust as needed
                    file_path=f"docs/{filename}"
                )
    print("Documents populated:", Document.objects.all())

if __name__ == "__main__":
    populate_documents()