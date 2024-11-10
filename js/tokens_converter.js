function tokens_converter_form (target, rubles) {
	tokens = rubles * 3;
	target.textContent = tokens;
}

function tokens_converter_menu (target, rubles) {
	tokens = rubles * 3;
	target.textContent = tokens;
}

let valueInputList = document.getElementsByClassName("form-input");
let tokensConverterList = document.getElementsByClassName("tokens-converter");