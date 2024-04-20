#from xmlrpc.client import ProtocolError
from django.db import models
from email.policy import default
from secrets import token_hex
from clientes.models import Cliente
from .choices import ChoicesCategoriaManutencao
from datetime import datetime


class CategoriaManutencao(models.Model):
    #Para adicionar mais campos de manutencao utilizar o arquivo choices.py na raiz do app
    titulo = models.CharField(max_length=3, choices=ChoicesCategoriaManutencao.choices)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.titulo

class Servico(models.Model):
    titulo = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete= models.SET_NULL, null=True)
    #usando relacao manytomany com a models categoria manutencao criada acima
    categoria_manutencao = models.ManyToManyField(CategoriaManutencao)

    data_inicio = models.DateField(null=True)
    data_entrega = models.DateField(null=True)
    finalizado = models.BooleanField(default=False)
    protocolo = models.CharField(max_length=52, null=True, blank=True)

    def __str__(self) -> str:
        return self.titulo
    
    def save(self, *args, **kwargs):
        #se o protocolo nao existir vai ser criado um novo protocolo
        if not self.protocolo:
            #criando novo protocolo usando como nome base a data e hora da criação e um token gerado pela biblioteca secrets do python, acada byte ela gera dois caracteres (na model o campo é de 52)
            self.protocolo = datetime.now().strftime("%d/%m/%Y-%H:%M:%S-") + token_hex(16)
        #Executando atravez do super o metodo save do models do Django, atrelado a este save criado
        super(Servico,self).save(*args, **kwargs)

    def preco_total(self):
        preco_total = float(0)
        #como categoria_m tem relacao MtM, para ter acesso iteiraveis aos seus objetos, é necessário ter o método.all para ter acesso
        for categoria in self.categoria_manutencao.all():
            preco_total += float(categoria.preco)

        return preco_total