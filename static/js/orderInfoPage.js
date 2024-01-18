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