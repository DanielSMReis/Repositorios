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
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]') //obtendo o token
    id_cliente = cliente.value

    data = new FornData()
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
        console.log('testee')
    })

}