from django.shortcuts import render
from .models import Home

def home(request):
    home = Home.objects.all().first()
    context = {
        'title': home.title,
        'text': home.text,
        'phone': home.phone,
        'email': home.email
    }
    
    return render(request, 'index.html', context)
