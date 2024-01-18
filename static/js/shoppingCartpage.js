const menu = document.querySelector(".menu-container");
const icon_menu = document.querySelector(".menu-icon");
const close_menu = document.querySelector(".closs-menu");
const about_link = document.querySelector(".about-link");
const product_link = document.querySelector(".product-link");

icon_menu.addEventListener("click", () => {
    menu.classList.remove("hide-menu");
})

close_menu.addEventListener("click", () => {
    menu.classList.add("hide-menu");
})

about_link.addEventListener("click", () => {
    menu.classList.add("hide-menu");
})

product_link.addEventListener("click", () => {
    menu.classList.add("hide-menu");
})

let add_btn = document.getElementsByClassName("add")
for (let i = 0; i < add_btn.length; i++) {
    add_btn[i].addEventListener("click", (e) => {
        let quantity = e.target.parentElement.querySelector('.quantity')
        let total_amount = e.target.parentElement.parentElement.querySelector(".total-amount")
        let original_amount = e.target.parentElement.parentElement.parentElement.querySelector(".price")

        let val = Number(quantity.innerHTML)
        let original = Number(original_amount.innerHTML)

        quantity.innerHTML = val + 1;
        total_amount.innerHTML = original * (val + 1)
        totalCalculator()
    })
}

let minu_btn = document.getElementsByClassName("minus")
for (let i = 0; i < add_btn.length; i++) {
    minu_btn[i].addEventListener("click", (e) => {
        let quantity = e.target.parentElement.querySelector('.quantity')
        let total_amount = e.target.parentElement.parentElement.querySelector(".total-amount")
        let original_amount = e.target.parentElement.parentElement.parentElement.querySelector(".price")

        let val = Number(quantity.innerHTML)
        let original = Number(original_amount.innerHTML)
        console.log(typeof (val))
        if (val <= 1) {
            val = 1
            quantity.innerHTML = val;
            total_amount.innerHTML = original * val
        }
        else {
            quantity.innerHTML = val - 1;
            total_amount.innerHTML = original * (val - 1)
        }
        totalCalculator()
    })
}

let delete_btn = document.getElementsByClassName("delete-btn")
for (let i = 0; i < delete_btn.length; i++) {
    delete_btn[i].addEventListener("click", (e) => {
        e.target.parentElement.remove();
        totalCalculator()
    })
}

function totalCalculator(){
    let prices = document.querySelectorAll(".total-amount")
    let grant_total = 0;
    prices.forEach(function (item) {
        grant_total = grant_total + Number(item.innerHTML)
        console.log(grant_total)
    })
    document.querySelector(".grant-total-amount").innerHTML = grant_total
}
totalCalculator()