const cep = document.querySelectorAll('#cep')
const matricula = document.querySelectorAll('#matrícula')
const numero_endereco = document.querySelectorAll('#numero')
const renda = document.querySelectorAll('#renda')
const idade = document.querySelectorAll('#idade')
const motivacao = document.querySelectorAll('#motivação')
const preco = document.querySelectorAll('#preco')
const id_notebook = document.querySelectorAll('#id_notebook')
const valor_disponivel = document.querySelectorAll('#valor_disponivel')
const porcentagem_gp = document.querySelectorAll('.porcentagem_gp')



for (const item of cep) {
    new Cleave(item, {
        blocks: [5, 3],
        delimiters: ['-'],
        numericOnly: true
    })
}


for (const item of matricula) {
    if (item.readOnly == false) {
        new Cleave(item, {
            blocks: [10],
            prefix: 'RA',
            numericOnly: true
        })
    }
}


for (const item of numero_endereco) {
    new Cleave(item, {
        blocks: [5],
        numericOnly: true
    })
}


for (const item of renda) {
    new Cleave(item, {
        numeral: true,
        numeralDecimalMark: ',',
        delimiter: '.',
    })
}


for (const item of idade) {
    new Cleave(item, {
        blocks: [3],
        numericOnly: true
    })
}


for (const item of motivacao) {
    new Cleave(item, {
        blocks: [2],
        numericOnly: true
    })
}


for (const item of preco) {
    new Cleave(item, {
        numeral: true,
        numeralDecimalMark: ',',
        delimiter: '.',
    })
}


for (const item of id_notebook) {
    new Cleave(item, {
        blocks: [3],
        numericOnly: true
    })
}


for (const item of valor_disponivel) {
    new Cleave(item, {
        numeral: true,
        numeralDecimalMark: ',',
        delimiter: '.',
    })
}


for (const item of porcentagem_gp) {
    new Cleave(item, {
        numeral: true,
        numeralDecimalMark: ',',
    })
}
