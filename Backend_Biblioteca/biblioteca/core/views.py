from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .models import Livro
from .serializers import LivroSerializer
import json
from django.http import JsonResponse, HttpResponse

@csrf_exempt
def livro_list_create(request):
    if request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LivroSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
def livro_detail(request, pk):
    try:
        livro = Livro.objects.get(pk=pk)
    except Livro.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LivroSerializer(livro)
        return JsonResponse(serializer.data)
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LivroSerializer(livro, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        livro.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    
    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
