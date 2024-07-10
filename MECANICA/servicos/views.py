from django.shortcuts import render, get_object_or_404
#importando o formulario local "." criado no backend
from .Forms import FormServico
from django.http import HttpResponse
from .models import Servico
# Create your views here.
def novo_servico(request):
    if request.method == "GET":
        #instanciando a classe 
        form = FormServico()
        #enviado o form para o html do app {'nome': variavel}
        return render(request, "novo_servico.html", {'form': form})
    elif request.method == "POST":
        #reinstanciando o form para salvar no backend os dados do formulario da pagina de novo serviço
        form = FormServico(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponse('Salvo com Sucesso')
        else:
            return render(request, 'novo_servico.html',{'form': form})
        
def listar_servico(request):
    if request.method == "GET":
        servicos = Servico.objects.all()
        #mandando a variavel local servico para o listar_sercivo.html note que sempre o contexto entre {}
        return render(request, 'listar_servico.html', {'servicos': servicos})
    
def servico(request, identificador): 
    #usando o GOO404 para caso o identificador nao exista, a pagina renderize o erro 404
    servico = get_object_or_404(Servico, identificador=identificador)
    return render(request, 'servico.html', {'servico': servico})