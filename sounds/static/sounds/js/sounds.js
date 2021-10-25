function onPageLoad() {
    inputs = document.getElementsByTagName("input")
    for(var i=0; i < inputs.length; i++) {
        if (inputs[i].type == "radio") {
            inputs[i].addEventListener("change", radioOnChange)
        }

    }
}


function radioOnChange() {
    this.form.submit()
}
