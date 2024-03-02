from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def clientes(request):
    if request.method == "GET":
        return render(request, 'clientes.html')     #por padrao o django ja procura dentro da pasta template
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')




        return HttpResponse('teste')