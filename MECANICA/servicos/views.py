from django.shortcuts import render, get_object_or_404
#importando o formulario local "." criado no backend
from .Forms import FormServico
from django.http import HttpResponse
from .models import Servico
from fpdf import FPDF
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

def gerar_os(request, identificador):
    servico = get_object_or_404(Servico, identificador = identificador)
    #instanciando a classe da biblioteca FPDF
    pdf = FPDF()
    #é necessário criar uma pagina, setando fonte e outros parametros para a criacao do arquivo
    pdf.add_page()
    #nome da fonte, formato(italico,negrito..), tamanho
    pdf.set_font('Arial', 'B', 16)
    #criando uma tablea
    pdf.set_fill_color(240,240,240)
    #para pdf_cell(altura,largura,titulo,borda(0/1), pular linha(0/1),alinhamento(L/C/R),cor de fundo(0/1))
    pdf.cell(35, 10, 'Cliente:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.cliente.nome}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Manutenções:', 1, 0, 'L',1)

    for manutencao in servico.categoria_manutencao.all():
        pdf.cell(0, 10, f'- {manutencao.get_titulo_display()}', 1, 1, 'L', 1)
    pdf.output('os.pdf')


    return HttpResponse(identificador)