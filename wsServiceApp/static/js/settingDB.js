$(document).ready(function(){
    EnviaTestaConexao({}, '/Manager/Painel/Configuracao/BD/Buscar', 'POST')
        .then((resposta)=>{
            var url = $('#urlbasedados').val(resposta['dados']['url']);
            var username = $('#Usuariobasedados').val(resposta['dados']['username']);
            var nomeDB = $('#Nomebasedados').val(resposta['dados']['nameDB']);
            var porta = $('#Portabasedados').val(resposta['dados']['porta']);
            var senha = $('#senhabasedados').val('');
        })
        .catch((error)=>{
            console.log(error)
        })



    $('#testaConexaoDB').click(()=>{
        var url = $('#urlbasedados').val();
        var username = $('#Usuariobasedados').val();
        var nomeDB = $('#Nomebasedados').val();
        var porta = $('#Portabasedados').val();
        var senha = $('#senhabasedados').val();

        entry = {
            "url": url,
            "username": username,
            "nomeDB": nomeDB,
            "porta": parseInt(porta),
            "senha": senha
        };
        EnviaTestaConexao(entry, '/Manager/Painel/Configuracao/BD/Testar', 'POST')
        .then((resposta)=>{
            console.log(resposta)
        })
        .catch((error)=>{
            console.log(error)
        })
    }); 
    
    

    $('#salvarConexaoDB').click(()=>{
        var url = $('#urlbasedados').val();
        var username = $('#Usuariobasedados').val();
        var nomeDB = $('#Nomebasedados').val();
        var porta = $('#Portabasedados').val();
        var senha = $('#senhabasedados').val();

        entry = {
            "url": url,
            "username": username,
            "nomeDB": nomeDB,
            "porta": parseInt(porta),
            "senha": senha
        };

        EnviaTestaConexao(entry, '/Manager/Painel/Configuracao/BD/Salvar', 'POST')
        .then((resposta)=>{
            console.log(resposta)
        })
        .catch((error)=>{
            console.log(error)
        })

    });
});


function EnviaTestaConexao(entry, url, method) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: method,
            data: JSON.stringify(entry),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            statusCode: {
                201: function () {
                   console.log("Código de retorno: 201")
                },
                200: function () {
                    console.log("Código de retorno: 200")
                },
                401: function () {
                    console.log("Código de retorno: 401")
                },
                500: function () {
                    console.log("Código de retorno: 500")
                },
            },
            success: function (data) {
                resolve(data)
            },
            error: function (error) {
                reject(error)
            }
        });
    });
}