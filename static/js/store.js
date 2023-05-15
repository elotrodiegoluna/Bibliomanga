const rangeInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".price-input input"),
progress = document.querySelector(".slider .progress");

let priceMin = document.getElementById("value-min"),
priceMax = document.getElementById("value-max");

let priceGap = 1000;

let minVal = 0,
    maxVal = 200000;

rangeInput.forEach(input =>{
    input.addEventListener("input", e =>{
        minVal = parseInt(rangeInput[0].value);
        maxVal = parseInt(rangeInput[1].value);

        if (maxVal - minVal < priceGap) {
            if (e.target.className === "range-min") {
                rangeInput[0].value = maxVal - priceGap;
            } else {
                rangeInput[1].value = minVal + priceGap;
            }
        } else {
            priceMin.innerText = priceFormat(minVal);
            priceMax.innerText = priceFormat(maxVal);
            progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
            progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
        // Aca filtrar por precio
        //pMin = minVal;
        FilterAll();
    });
});

const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'CLP',
});

function priceFormat(value) {
    return formatter.format(value).toString().replace('CLP', '$');
}

// Filtrar por nombre
function FilterAll() {
    const input = document.querySelector(".form-control");
    const cards = document.getElementsByClassName("col-lg-3");
    let filter = input.value.toUpperCase();
    

    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].querySelector(".manga-nombre"),
        price = parseInt(cards[i].querySelector(".manga-precio").innerText.replace(/[CLP$,]/g, ''));
        
        if (title.innerText.toUpperCase().indexOf(filter) > -1) {
            cards[i].classList.remove("d-none");
            if (price >= minVal && price <= maxVal) { // anidar filtros
                cards[i].classList.remove("d-none");
            } else {
                cards[i].classList.add("d-none");
            }
        } else {
            cards[i].classList.add("d-none");
        }
    }
}
