function Envia(entry, url, method) {
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