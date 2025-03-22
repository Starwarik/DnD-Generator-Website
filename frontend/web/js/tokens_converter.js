let tokensConverterList = document.getElementsByClassName("tokens-converter");

function tokens_converter (className) {
	let element = document.getElementsByClassName(className)[0];

	switch (className) {
		case "value-input__account-menu":
			var tokensConverterElement = tokensConverterList[0];
			var rubles = element.value;
			var tokens = rubles;
			tokensConverterElement.textContent = tokens.toFixed(2);
			break;
		case "value-input__form":
			var tokensConverterElement = tokensConverterList[1];
			var rubles = element.value;
			var tokens = rubles;
			tokensConverterElement.textContent = tokens.toFixed(2);
			break;
	}
}