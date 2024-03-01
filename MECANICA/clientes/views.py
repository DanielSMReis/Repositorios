from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def clientes(request):
    return HttpResponse('Estou em clientes')