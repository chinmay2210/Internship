
// ____________________________________________________
//         loading animation of first section
// ____________________________________________________

function loadingAnimation() {
    gsap.from(".page1 h1", {
        y: 100,
        opacity: 0,
        delay: 0.5,
        duration: 0.5,
        stagger: 0.3,
    });
    gsap.from(".page2", {
        y: 100,
        opacity: 0,
        delay: 1.5,
        duration: 0.5
    });
}
loadingAnimation();


// ____________________________________________________
//        cursor animation for the product page
// ____________________________________________________
function cursorAnimation() {
    document.addEventListener("mousemove", function (dets) {
        gsap.to("#cursor", {
            left: dets.x,
            top: dets.y,
        });
    });

    document.querySelectorAll(".product-card").forEach(function (elem) {
        elem.addEventListener("mouseenter", function () {
            gsap.to("#cursor", {
                transform: "translate(-50%,-50%) scale(1)",
            });
        });
        elem.addEventListener("mouseleave", function () {
            gsap.to("#cursor", {
                transform: "translate(-50%,-50%) scale(0)",
            });
        });
    });
}
cursorAnimation();

// var swiper = new Swiper(".mySwiper", {
//     slidesPerView: 1,
//     spaceBetween: 20,
//     autoplay: {
//         delay: 2500,
//         disableOnInteraction: false,
//     },
//     pagination: {
//         el: ".swiper-pagination",
//         clickable: true,
//     },
// });

const myJsmedia = (widthSize) => {
    if (widthSize.matches) {
        new Swiper(".mySwiper", {
            slidesPerView: 1,
            spaceBetween: 20,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });
    } else {
        new Swiper(".mySwiper", {
            slidesPerView: 2,
            spaceBetween: 20,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });
    }
};

const widthSize = window.matchMedia("(max-width: 780px)");
myJsmedia(widthSize);
widthSize.addEventListener("change", myJsmedia);

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