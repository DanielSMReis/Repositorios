from django.shortcuts import render
#importando o formulario local "." criado no backend
from .Forms import FormServico

# Create your views here.
def novo_servico(request):
    #instanciando a classe 
    form = FormServico()
    #enviado o form para o html do app {'nome': variavel}
    return render(request, "novo_servico.html", {'form': form})