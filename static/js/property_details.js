document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".carousel-image");
    const leftBtn = document.querySelector(".carousel-nav.left");
    const rightBtn = document.querySelector(".carousel-nav.right");

    let currentIndex = 0;

    function showImage(index) {
        images.forEach((img, i) => {
            img.classList.remove("active");
            if (i === index) img.classList.add("active");
        });
    }

    leftBtn.addEventListener("click", function () {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage(currentIndex);
    });

    rightBtn.addEventListener("click", function () {
        currentIndex = (currentIndex + 1) % images.length;
        showImage(currentIndex);
    });
});
