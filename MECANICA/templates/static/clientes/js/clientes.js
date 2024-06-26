function add_carro(){

    container = document.getElementById('form-carro')

    html = "<br>  <div class='row'> <div class='col-md'> <input type='text' placeholder='carro' class='form-control' name='carro' > </div> <div class='col-md'><input type='text' placeholder='Placa' class='form-control' name='placa' ></div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='ano'> </div> </div>"
    
    container.innerHTML += html
}


function exibir_form(tipo){

    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')
    
    if(tipo == "1"){
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"

    }else if (tipo == "2"){
        att_cliente.style.display = "block"
        add_cliente.style.display = "none"

    }
    
}


function dados_clientes(){
    cliente = document.getElementById('cliente-select')

    //utilizando FETCH é uma forma de fazer requisiçoes para um endpoint em um determinado backend
    //precisa passar o dominio para o qual sera passado a requisição, depois os dados(method)
    //quando precisamos passar uma req HTTP precisamos enviar dois tipos de dados para o backend que é o cabeçalho e o corpo da req
    //as funçoes do django exigem que seja passada no corpo da req o csrftoken, que esta sendo gerada em clientes.html linha 22 (esse token gera um value unico que pode ser usado para referenciar a função)
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value //obtendo o VALOR do token
    id_cliente = cliente.value

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/",{
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,  //garantimos que nao havera falsificação de formulários
        },
        body: data
    }).then(function(result){//depois de enviar a req, o servidor vai mandar uma resposta, por isso isamos o .then para aguardar essa resposta, depois esta é passada para function e convertida em um json
        return result.json()

    }).then(function(data){
        aux = document.getElementById('form-att-cliente')
        aux.style.display = 'block'

        id = document.getElementById('id')
        id.value = data['cliente_id']
        
        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['cliente']['sobrenome']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ""

        for (i=0; i < data['carros'].length; i++){
            div_carros.innerHTML += "\<form action='/clientes/update_carro/" + data['carros'][i]['id'] +"' method='POST'>\
                <div class = 'row'>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='carro' value= '" + data['carros'][i]['fields']['carro']+"'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='placa' value= '" + data['carros'][i]['fields']['placa']+"'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='ano' value= '" + data['carros'][i]['fields']['ano'] +"' >\
                        </div>\
                        <div class='col-md'>\
                            <input class='btn btn-success' type='submit' value = 'SALVAR'>\
                        </div>\
                    </form>\
                    <div class='col-md'>\
                        <a href='/clientes/excluir_carro/"+ data['carros'][i]['id'] +"' class ='btn btn-danger' >EXCLUIR</a>\
                    </div>\
                </div><br>"
            
        }

    })

}

function update_cliente(){
    id = document.getElementById('id').value
    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value
    //enviando os dados do cliente.html para o backend usando o fetch
    fetch('/clientes/update_cliente/' +id, {

        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf
        })

    }).then(function(result){
        return result.json()
    }).then(function(data){

        if (data['status'] == '200'){
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']
            console.log('registro do cliente alterado com sucesso')
        }else{
            console.log('ERRO AO SALVAR')
        }
        
    })

}