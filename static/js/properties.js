document.addEventListener('DOMContentLoaded', function() {
    // Handle favorite icon clicks
    document.querySelectorAll('.favorite-icon').forEach(icon => {
        icon.addEventListener('click', function(e) {
            // Toggle the active class
            this.classList.toggle('active');
            
            // Check if we're using Font Awesome icons
            const heartIcon = this.querySelector('i');
            
            if (heartIcon) {
                // Font Awesome icon approach
                if (this.classList.contains('active')) {
                    heartIcon.classList.replace('fa-regular', 'fa-solid');
                } else {
                    heartIcon.classList.replace('fa-solid', 'fa-regular');
                }
            } else {
                // Plain HTML approach - toggle between empty and filled heart entities
                if (this.classList.contains('active')) {
                    this.innerHTML = '♥'; // Filled heart
                } else {
                    this.innerHTML = '&#9825;'; // Outline heart
                }
            }
            
            // Prevent the click from bubbling up to the parent
            e.stopPropagation();
            e.preventDefault();
            
            // Here you would normally add AJAX to save the favorite status
            console.log('Favorite toggled');
        });
    });
    
    // Make property cards clickable
    document.querySelectorAll('.property-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't redirect if the favorite icon was clicked
            if (e.target.closest('.favorite-icon')) {
                return;
            }
            
            // Get the property ID from the data attribute
            const propertyId = this.getAttribute('data-id');
            if (propertyId) {
                window.location.href = `/properties/${propertyId}/`;
            }
        });
    });
});