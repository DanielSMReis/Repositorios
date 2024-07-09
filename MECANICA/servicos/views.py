from django.shortcuts import render
#importando o formulario local "." criado no backend
from .Forms import FormServico
from django.http import HttpResponse
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