document.addEventListener('DOMContentLoaded', function() {
    // Handle favorite icon clicks
    document.querySelectorAll('.favorite-icon').forEach(icon => {
        icon.addEventListener('click', function(e) {
            // Toggle the active class
            this.classList.toggle('active');

            // Toggle between solid and regular heart
            const heartIcon = this.querySelector('i');
            if (this.classList.contains('active')) {
                heartIcon.classList.replace('fa-regular', 'fa-solid');
            } else {
                heartIcon.classList.replace('fa-solid', 'fa-regular');
            }

            // Prevent the click from bubbling up to the parent
            e.stopPropagation();
            e.preventDefault();

            // Here you would normally add AJAX to save the favorite status
            console.log('Favorite toggled');
        });
    });

    // Rest of the code for property cards...
});