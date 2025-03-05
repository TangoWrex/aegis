import os
import sys
import django
from django.conf import settings
from PyPDF2 import PdfReader

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appServer.settings")
django.setup()

# Import models after setup
from search.models import Document

def load_documents():
    doc_dir = os.path.join(settings.BASE_DIR, 'static', 'docs')
    if not os.path.exists(doc_dir):
        os.makedirs(doc_dir)
        print("Created docs/ folder. Add your READMEs and PDFs there.")
        return

    for filename in os.listdir(doc_dir):
        file_path = os.path.join(doc_dir, filename)
        if Document.objects.filter(title=filename).exists():
            continue  

        if filename.endswith('.pdf'):
            reader = PdfReader(file_path)
            content = ""
            for page in reader.pages:
                content += page.extract_text() or ""
        elif filename.endswith('.md') or filename.endswith('.txt'):
            with open(file_path, 'r') as f:
                content = f.read()
        else:
            continue

        Document.objects.create(title=filename, content=content, file_path=file_path)
        print(f"Loaded {filename}")

if __name__ == "__main__":
    load_documents()