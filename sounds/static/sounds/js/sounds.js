function onPageLoad() {
    inputs = document.getElementsByTagName("input")
    for(var i=0; i < inputs.length; i++) {
        if (inputs[i].type == "radio") {
            inputs[i].addEventListener("change", radioOnChange)
        }
    }

    buttons = document.getElementsByClassName("rating_button")
    for(i = 0; i < buttons.length; i++) {
        buttons[i].style.display = 'none'
    }
}


function radioOnChange() {
    this.form.submit()
}
