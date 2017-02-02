const product_name = document.querySelector('#inputName');
const product_count = document.querySelector('#inputCount');
const product_address = document.querySelector('#inputAddress');
const product_date = document.querySelector('#inputDate');
v = document.querySelector('#inputDate').value;


const submit_button = document.querySelector('#submitButton');

function count_changed() {
    console.log(this.value);
    if (product_count.value < 1 || product_count.value > 10) {
        this.classList.add('invalid');
        invalid(this);
    } else {
        valid(this);
    }
}

function address_changed() {
    console.log(this.value);
    val = product_address.value.length;
    if (val < 7 || val > 200) {
        alert("address incorrect!");
        invalid(this);
    } else {
        valid(this);
    }
}

function date_changed() {
    str = this.value + 'z';
    date = new Date(str);
    if (date < Date.now()) {
        alert("date incorrect!");
        invalid(this);
    } else {
        valid(this);
    }
}

function name_changed() {
    if (this.length < 4) {
        alert("name short");
        invalid(this);
    } else {
        valid(this);
    }
}

function invalid(elem) {
    elem.classList.add('invalid');
    submit_button.classList.add('invalidButton');
    submit_button.disabled = true;
}

function valid(elem) {
    elem.classList.remove('invalid');
    submit_button.classList.remove('invalidButton');
    if (!product_address.classList.contains('invalid') &&
        !product_date.classList.contains('invalid') &&
        !product_count.classList.contains('invalid')) {
        submit_button.disabled = false;
    }
}


product_name.onchange = name_changed;
product_count.onchange = count_changed;
product_address.onchange = address_changed;
product_date.onchange = date_changed;
