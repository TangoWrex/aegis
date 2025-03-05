from django.shortcuts import render
from django.db.models import Q
from .models import Document

def search_view(request):
    query = request.GET.get('q', '').strip()
    results = []
    all_docs = Document.objects.all()  # List all docs
    if query:
        results = Document.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    return render(request, 'search.html', {
        'query': query,
        'results': results,
        'all_docs': all_docs
    })