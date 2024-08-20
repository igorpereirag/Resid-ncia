from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .models import Livro
from .serializers import LivroSerializer
import json

@csrf_exempt
def livro_list_create(request):
    if request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = LivroSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return HttpResponse(status=405)

@csrf_exempt
def livro_detail(request, pk):
    try:
        livro = Livro.objects.get(pk=pk)
    except Livro.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = LivroSerializer(livro)
        return JsonResponse(serializer.data)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        serializer = LivroSerializer(livro, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    if request.method == 'DELETE':
        livro.delete()
        return HttpResponse(status=204)
    return HttpResponse(status=405)
