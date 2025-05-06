document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.nav-bar');
    let lastScrollTop = 0;
    const scrollThreshold = 10; // Minimum amount of pixels to scroll before showing/hiding

    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Determine scroll direction and amount
        if (Math.abs(lastScrollTop - scrollTop) <= scrollThreshold) {
            return; // Ignore small scroll movements
        }

        // Hide when scrolling down, show when scrolling up
        if (scrollTop > lastScrollTop && scrollTop > navbar.offsetHeight) {
            // Scrolling DOWN past the navbar height
            navbar.classList.add('nav-bar--hidden');
        } else {
            // Scrolling UP
            navbar.classList.remove('nav-bar--hidden');
        }

        lastScrollTop = scrollTop;
    });
});
