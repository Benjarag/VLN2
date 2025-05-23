document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.favorite-icon').forEach(icon => {
        icon.addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();

            const wasActive = this.classList.contains('active');
            
            // First try to get ID from the favorite icon itself
            let propertyId = this.getAttribute('data-id');
            
            // If not found, try to get it from the parent property card
            if (!propertyId) {
                const propertyCard = this.closest('.property-card');
                propertyId = propertyCard?.getAttribute('data-id');
            }
            
            // If still no ID, log error and return
            if (!propertyId) {
                console.error('No property ID found for favorite action');
                return;
            }
            
            const heartIcon = this.querySelector('i');

            this.classList.toggle('active');

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

            fetch('/accounts/toggle-favorite/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: `property_id=${propertyId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'guest-user') {
                    this.classList.toggle('active', wasActive);
                    if (heartIcon) {
                        heartIcon.classList.toggle('fa-regular', !wasActive);
                        heartIcon.classList.toggle('fa-solid', wasActive);
                    } else {
                        this.innerHTML = wasActive ? '♥' : '&#9825;';
                    }

                    const popup = document.getElementById('login-popup');
                    const backdrop = document.getElementById('popup-backdrop');
                    if (popup) popup.style.display = 'block';
                    if (backdrop) backdrop.style.display = 'block';
                    return;
                }

                if (data.status === 'added' && !this.classList.contains('active')) {
                    this.classList.add('active');
                } else if (data.status === 'removed' && this.classList.contains('active')) {
                    this.classList.remove('active');
                }
            })
            .catch(error => {
                console.error('Error toggling favorite:', error);
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
});