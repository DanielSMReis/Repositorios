from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404


def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(
            request, "clientes.html", {"clientes": clientes_list}
        )  # por padrao o django ja procura dentro da pasta template
    elif request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        carros = request.POST.getlist("carro")
        placas = request.POST.getlist("placa")
        anos = request.POST.getlist("ano")

        # testando se cliente ja existe
        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(
                request,
                "clientes.html",
                {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "carros": zip(carros, placas, anos),
                },
            )

        if not re.fullmatch(
            re.compile(
                r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            ),
            email,
        ):
            return render(
                request,
                "clientes.html",
                {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "cpf": cpf,
                    "carros": zip(carros, placas, anos),
                },
            )
        # AT 1:28:40#1
        # importando a classe cliente migrada para banco de dados(primeiro precisa ter cliente para ter um carro, lembre-se)

        cliente = Cliente(nome=nome, sobrenome=sobrenome, email=email, cpf=cpf)
        cliente.save()

        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()

        return HttpResponse("teste")


##como esta requisição esta iniciada com javascript para nao ser reenderizada em html e passar somente os dados passamos via Json (jsonresponse)
def att_cliente(request):
    id_cliente = request.POST.get("id_cliente")

    # pegando os dados do cliente cuja id foi passada pela request do model Cliente(BdD)
    cliente = Cliente.objects.filter(id=id_cliente)
    # capturando o carro do cliente, como o filter retorna um objeto com varios parametros, o label 0 de cliente seleta apenas o nome do cliente
    carros = Carro.objects.filter(cliente=cliente[0])

    # usando o serializador do djamgo para importar os dados do cliente e de seus respectivos carros em formato json
    cliente_json = json.loads(serializers.serialize("json", cliente))[0]["fields"]
    #criando id do cliente atraves da chave pk 
    cliente_id = json.loads(serializers.serialize("json", cliente))[0]['pk']

    carros_json = json.loads(serializers.serialize("json", carros))

    # coletando somente as informaçoes do carro e seu respectivo id em PK
    carros_json = [
        {"fields": carro["fields"], "id": carro["pk"]} for carro in carros_json
    ]

    data = {"cliente": cliente_json, "carros": carros_json, 'cliente_id': cliente_id}
    return JsonResponse(data)


@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get("carro")
    placa = request.POST.get("placa")
    ano = request.POST.get("ano")

    carro = Carro.objects.get(id=id)
    lista_carros = Carro.objects.filter(placa=placa).exclude(id=id)
    if lista_carros.exists():
        return HttpResponse("Placa ja existe!")

    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()
    print(carro)
    return HttpResponse(f"Os dados do {nome_carro} foram alterados com sucesso!")


def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        # concatenando f'?aba=attcliente e(&) a informação do id do cliente que foi alterado
        return redirect(reverse("clientes") + f"?aba=att_cliente&id_cliente={id}")
    except:
        return redirect(reverse("clientes") + f"?aba=att_cliente&id_cliente={id}")

#como o backend recebe o ID pela URL, o que faz com que a tratativa seja feita no clientes.js
def update_cliente(request, id):
    #convertendo os dados binarios armazenados na req. para json
    body = json.loads(request.body)
    nome = body['nome']
    sobrenome = body['sobrenome']
    email = body['email']
    cpf = body['cpf']
    
    #usando o get_object_or_404 para buscar no banco de dados local qual cliente será atualizado
    cliente = get_object_or_404(Cliente, id=id) #comando getobjector404 = (qual model,qual coluna = compar com)
    #carregando novos valores e salvando no model
    try: ######## FAZER AS REVALIDAÇOES DOS DADOS ABAIXO!############
        cliente.nome = nome    
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse({'status': 200, 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
    except:
        return JsonResponse({'status':500})