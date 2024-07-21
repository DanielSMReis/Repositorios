from django.shortcuts import render, get_object_or_404
#importando o formulario local "." criado no backend
from .Forms import FormServico
from django.http import HttpResponse, FileResponse
from .models import Servico, ServicoAdicional
from fpdf import FPDF
from io import BytesIO
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
    pdf.set_font('Arial', 'B', 12)
    #criando uma tablea
    pdf.set_fill_color(240,240,240)
    #para pdf_cell(altura,largura,titulo,borda(0/1), pular linha(0/1),alinhamento(L/C/R),cor de fundo(0/1))
    pdf.cell(36, 10, 'Cliente:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.cliente.nome}', 1, 1, 'L', 1)
    pdf.cell(36, 10, 'Manutenções:', 1, 0, 'L',1)

    enumerar_categorias = servico.categoria_manutencao.all()
    for i, manutencao in enumerate(enumerar_categorias):
        pdf.cell(0, 10, f'- {manutencao.get_titulo_display()}', 1, 1, 'L', 1)
        if not i == len(enumerar_categorias) -1:
            pdf.cell(36,10, '',0,0)
    

    pdf.cell(36,10, 'Data de início:', 1, 0,'L',1)
    pdf.cell(0,10, f'{servico.data_inicio}', 1,1,'L',1)
    pdf.cell(36,10, 'Data de entrega:', 1, 0,'L',1)
    pdf.cell(0,10, f'{servico.data_entrega}', 1,1,'L',1)
    pdf.cell(36,10, 'Protocolo:', 1, 0,'L',1)
    pdf.cell(0,10, f'{servico.protocolo}', 1,1,'L',1)
    pdf.cell(36,10, 'Preço total:', 1, 0,'L',1)
    pdf.cell(0,10, f'{servico.preco_total()}', 1,1,'L',1)
    
    #Salvando o arquivo PDF em memoria para que seja exibido para os demais usuarios do sistema.
    #Usando o parametro "dest=S" definimos que estaremos salvando em memoria.
    #como a função nao devolve uma str, precisa codificar usando o encode
    pdf_content = pdf.output(dest='S').encode('latin1')

    #como o django nao consegue retornar o arquivo em response http, é necessário fazer com que ele leia de fato o arquivo usando o FileResponse. 
    #para isto, é necessario passar o arquivo e os bytes dele, usando o bytesIO da biblioteca IO do python
    pdf_bytes = BytesIO(pdf_content)
    #Para salvar automaticamente o PDF, basta por o parametro: "as_attachment=True" antes de filename.
    return FileResponse(pdf_bytes, filename=f"os-{servico.protocolo}.pdf")


def servico_adicional(request):
    identificador_servico = request.POST.get('identificador_servico')
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    preco = request.POST.get('preco')

    servico_adicional = ServicoAdicional(titulo = titulo, descricao = descricao, preco = preco)
    servico_adicional.save()

    #criando um link entre o servico adicional e os servicos do cliente
    servico = Servico.objects.get(identificador = identificador_servico)
    servico.servicos_adicionais.add(servico_adicional)
    servico.save()

    return HttpResponse("Salvo")