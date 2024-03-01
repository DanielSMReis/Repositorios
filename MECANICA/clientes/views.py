from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def clientes(request):
    return render(request, 'clientes.html')     #por padrao o django ja procura dentro da pasta template