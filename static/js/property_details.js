document.addEventListener("DOMContentLoaded", function () {
    const imagesContainer = document.querySelector(".carousel-images");
    const images = document.querySelectorAll(".carousel-image");
    const leftBtn = document.querySelector(".carousel-nav.left");
    const rightBtn = document.querySelector(".carousel-nav.right");

    let currentIndex = 0;

    function updateCarousel() {
        const offset = -currentIndex * 100;
        imagesContainer.style.transform = `translateX(${offset}%)`;
    }

    leftBtn.addEventListener("click", function () {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateCarousel();
    });

    rightBtn.addEventListener("click", function () {
        currentIndex = (currentIndex + 1) % images.length;
        updateCarousel();
    });

    updateCarousel();
});
