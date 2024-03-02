from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Carro
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