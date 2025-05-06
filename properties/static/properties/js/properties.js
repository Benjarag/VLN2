document.querySelectorAll('.favorite-icon').forEach(icon => {
    icon.addEventListener('click', () => {
        icon.classList.toggle('active');
        const heartIcon = icon.querySelector('i');
        if (icon.classList.contains('active')) {
            heartIcon.classList.replace('fa-regular', 'fa-solid');
        } else {
            heartIcon.classList.replace('fa-solid', 'fa-regular');
        }
    });
});

// Redirect when clicking a property card (except on the heart)
document.querySelectorAll('.property-card').forEach(card => {
    card.addEventListener('click', (e) => {
        // Prevent redirect if heart icon is clicked
        if (e.target.closest('.favorite-icon')) return;

        const propertyId = card.dataset.id;
        if (propertyId) {
            window.location.href = `/properties/${propertyId}/`;
        }
    });
});


