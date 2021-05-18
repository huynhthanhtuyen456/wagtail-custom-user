from django.shortcuts import render

# Create your views here.

def schema_url(request):
    return render(request, 'openapi-schema.yml')