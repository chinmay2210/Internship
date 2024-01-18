document.addEventListener("DOMContentLoaded", function() {
    const plus = document.querySelector(".plus");
    const minus = document.querySelector(".minus");
    const num = document.querySelector(".num");

    let quantity = 1;

    plus.addEventListener("click", () => {
        quantity++;
        quantity = (quantity < 10) ? "0" + quantity : quantity;
        num.innerText = quantity;
        updateHref(quantity);
    });

    minus.addEventListener("click", () => {
        if (quantity > 1) {
            quantity--;
            quantity = (quantity < 10) ? "0" + quantity : quantity;
            num.innerText = quantity;
            updateHref(quantity);
        }
    });

    function updateHref(quantity) {
        const href = '/addtocart/' + quantity;
        document.querySelector('.btn').href = href;
    }
});