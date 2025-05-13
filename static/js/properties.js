document.addEventListener('DOMContentLoaded', function() {
    // Handle favorite icon clicks
    document.querySelectorAll('.favorite-icon').forEach(icon => {
        icon.addEventListener('click', function(e) {
            // Prevent default and propagation first
            e.stopPropagation();
            e.preventDefault();

            // Store initial state in case we need to rollback
            const wasActive = this.classList.contains('active');
            const propertyCard = this.closest('.property-card');
            const propertyId = propertyCard?.getAttribute('data-id');
            const heartIcon = this.querySelector('i');

            // Immediately toggle UI state
            this.classList.toggle('active');

            // Update visual state
            if (heartIcon) {
                heartIcon.classList.toggle('fa-regular');
                heartIcon.classList.toggle('fa-solid');
            } else {
                this.innerHTML = this.classList.contains('active') ? '♥' : '&#9825;';
            }

            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            // Send request to server
            fetch('/accounts/toggle-favorite/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: `property_id=${propertyId}`
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // The guest user should still be able to see the UI effect, but we don't save it
                if (data.status === 'guest-user') {
                    // Roll back the visual state
                    this.classList.toggle('active', wasActive);
                    if (heartIcon) {
                        heartIcon.classList.toggle('fa-regular', !wasActive);
                        heartIcon.classList.toggle('fa-solid', wasActive);
                    } else {
                        this.innerHTML = wasActive ? '♥' : '&#9825;';
                    }

                    // Show the popup
                    const popup = document.getElementById('login-popup');
                    if (popup) popup.style.display = 'block';
                    return;
                }

                console.log(`Favorite ${data.status} for property ID: ${propertyId}`);
                // Update UI based on server response if needed
                if (data.status === 'added' && !this.classList.contains('active')) {
                    this.classList.add('active');
                } else if (data.status === 'removed' && this.classList.contains('active')) {
                    this.classList.remove('active');
                }
            })
            .catch(error => {
                console.error('Error toggling favorite:', error);
                // Rollback UI changes
                this.classList.toggle('active', wasActive);
                if (heartIcon) {
                    heartIcon.classList.toggle('fa-regular', !wasActive);
                    heartIcon.classList.toggle('fa-solid', wasActive);
                } else {
                    this.innerHTML = wasActive ? '♥' : '&#9825;';
                }
            });
        });
    });

    // Property card click handler remains the same
    document.querySelectorAll('.property-card').forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.closest('.favorite-icon')) return;
            const propertyId = this.getAttribute('data-id');
            if (propertyId) window.location.href = `/properties/${propertyId}/`;
        });
    });
});