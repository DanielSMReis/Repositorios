from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import Servico, CategoriaManutencao

#criando um formulario usand o recurs ModelForm do Django, os campos do formulário ja vem definidos de acordo com a classe ancestral
#sintetizando: crie um formulário baseado numa model, quaal model? detro de Meta
class FormServico (ModelForm):
    #classe obrigatoria padrao de configuraçao
    class Meta:
        #qual classe sera usada como base para criaçao do formlario?
        model = Servico
        #quais campos serao os que vao compor os Fields do Form?
        #usando exclude, excluimos apenas os campos que nao serao editáveis para o usuario
        exclude = ['finalizado', 'protocolo']
        #para mandar para o frontend é necessario importar este arquivo no views do app
    
    #rescrevendo o método init da classe para personalizar a apresentação do form
    def __init__(self, *args, **kwargs):
        #execussao obrigatória do super para sobrescrever o innit desta classe, precisamos referenciar a sobrescriçao na classe ancestral usando o "super"
        super().__init__(*args, **kwargs)
        #acessando o diionario python retornado do self.fields e adicionando um novo atributo em todos os campos, uma classe do bootstrap(manipulando html com python)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'placeholder': field})