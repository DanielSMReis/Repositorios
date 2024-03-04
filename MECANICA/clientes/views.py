from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Carro
import re
# Create your views here.
def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})     #por padrao o django ja procura dentro da pasta template
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')
        #testando se cliente ja existe
        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'email':email, 'carros': zip(carros, placas, anos)})
        
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email): 
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'cpf':cpf, 'carros': zip(carros, placas, anos)})
        #AT 1:28:40#1
        #importando a classe cliente migrada para banco de dados(primeiro precisa ter cliente para ter um carro, lembre-se)
        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )
        cliente.save()
        # X = list(zip(carros, placas, anos)) #concatenando e correlacionando cada carro com seus respectivos dados com a função zip e transformando em lista para retirar os numeros de memoria
        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()

        return HttpResponse('teste')