const cepInputs = document.querySelectorAll('input#cep')
for (const item of cepInputs) {
    item.addEventListener('blur', function () {
        buscacep(item)
    })
}



function buscacep(input) {
    const cep = input.value
    const url = `https://brasilapi.com.br/api/cep/v2/${cep}`
    const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
            'content-type': 'application/json;charset=utf-8'
        }
    }

    if(!input.validity.valueMissing) {
        fetch(url, options).then(
            response => response.json()
        ).then(
            data => {
                buscacep_fill(data)
                return
            }
        )
    }
}



function buscacep_fill(data) {
    const logradouro = document.querySelector('#logradouro')
    const bairro = document.querySelector('#bairro')
    const cidade = document.querySelector('#cidade')
    const estado = document.querySelector('#uf')
    const pais = document.querySelector('#pais')

    logradouro.value = data.street
    /*logradouro.readOnly = true
    logradouro.tabIndex = '-1'*/

    bairro.value = data.neighborhood
    /*bairro.readOnly = true
    bairro.tabIndex = '-1'*/

    cidade.value = data.city
    cidade.readOnly = true
    cidade.tabIndex = '-1'

    estado.value = data.state
    estado.readOnly = true
    estado.tabIndex = '-1'

    pais.value = 'Brasil'
    pais.readOnly = true
    pais.tabIndex = '-1'
}
