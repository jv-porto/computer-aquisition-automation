const nav = document.querySelector('nav')


/*************** SHOW MENU ***************/
const logo = document.querySelectorAll('.logo')
for (const item of logo) {
    item.addEventListener('click', function () {
        nav.classList.toggle('show-menu')
    })
}



/*************** SHOW PESQUISAR ***************/
const page_actions_pesquisar = document.querySelectorAll('div.page-actions .page-actions-pesquisar')
for (const item of page_actions_pesquisar) {
    item.addEventListener('click', function () {
        nav.classList.toggle('show-pesquisar')
    })
}



/*************** ADD SEARCH FILTER ***************/
const search_input = document.querySelectorAll('div.pesquisar form input#search')
const search_form = document.querySelectorAll('div.pesquisar form')
for (const item of search_input) {
    item.addEventListener('blur', function () {
        for (const form of search_form) {
            form.action = `?search=${item.value}`
        }
    })
}



/*************** HIDE PESQUISAR ***************/
const pesquisar_actions_close = document.querySelectorAll('div.pesquisar .pesquisar-actions-close')
for (const item of pesquisar_actions_close) {
    item.addEventListener('click', function () {
        nav.classList.toggle('show-pesquisar')
    })
}



/*************** SHOW DROPDOWN MENU ***************/
const dropdown = document.getElementsByClassName("dropdown-button")
for (let i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener('click', function () {
        this.classList.toggle('active')
        var dropdownContent = this.nextElementSibling
        if (dropdownContent.style.display === 'block') {
            dropdownContent.style.display = 'none'
        } else {
            dropdownContent.style.display = 'block'
        }
    })
}



/*************** SHOW PROFILE ***************/
const profileSection = document.getElementsByClassName("profile-image")
for (const item of profileSection) {
    item.addEventListener('click', function () {
        item.classList.toggle('open')
    })
}



/*************** SHOW PAGE ACTIONS DROPDOWN SECTION ***************/
const pageActionsDropdownSection = document.getElementsByClassName("page-actions-incluir")
for (const item of pageActionsDropdownSection) {
    item.addEventListener('click', function () {
        item.classList.toggle('open')
    })
}



/*************** CHOOSE ID FOR MENU ACTIONS ***************/
const clickable_tr = document.querySelectorAll('.clickable-tr')
for (const item of clickable_tr) {
    item.addEventListener('click', function () {
        idValue = item.children[0].value
        window.location.href = `${idValue}`
    })
}



/*************** GET SELECT INFO ***************/
const select_value = document.querySelectorAll('form div.form-section div.input-unit input.select-value[type=hidden]')
if (select_value) {
    for (const item of select_value) {
        const option = document.querySelector(`form div.form-section div.input-unit select#${item.id} option[value="${item.value}"]`)
        option.selected = true
    }
}
