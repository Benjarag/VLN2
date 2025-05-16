document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
    const yyyy = today.getFullYear();

    const minDate = yyyy + '-' + mm + '-' + dd;
    document.getElementById('expiration_date').min = minDate;

    // Set default date to 7 days from now
    const nextWeek = new Date(today);
    nextWeek.setDate(today.getDate() + 7);
    const nextWeekDD = String(nextWeek.getDate()).padStart(2, '0');
    const nextWeekMM = String(nextWeek.getMonth() + 1).padStart(2, '0');
    const nextWeekYYYY = nextWeek.getFullYear();

    const defaultDate = nextWeekYYYY + '-' + nextWeekMM + '-' + nextWeekDD;
    document.getElementById('expiration_date').value = defaultDate;

    // Form submission handling
    const form = document.getElementById('purchase-offer-form');
    const modal = document.getElementById('confirmation-modal');
    const closeButton = document.querySelector('.close-button');
    const modalOkButton = document.getElementById('modal-ok-button');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);

        // Check terms agreement
        if (!formData.get('terms_agreement')) {
            showModal('Error', 'You must agree to the terms to proceed.', false);
            return;
        }

        // Validate offer price
        const offerPrice = formData.get('offer_price');
        if (!offerPrice || offerPrice <= 0) {
            showModal('Error', 'Please enter a valid offer amount.', false);
            return;
        }

        // Send AJAX request
        fetch("{% url 'offers:submit_purchase_offer' property_id=property.id %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showModal('Success', data.message, true);
            } else {
                showModal('Error', data.message, false);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModal('Error', 'An unexpected error occurred. Please try again.', false);
        });
    });

    function showModal(title, message, isSuccess) {
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-message').textContent = message;

        if (isSuccess) {
            modalOkButton.href = "{% url 'properties:property_details' property_id=property.id %}";
        } else {
            modalOkButton.href = "#";
            modalOkButton.onclick = function() {
                modal.style.display = "none";
                return false;
            };
        }

        modal.style.display = "block";
    }

    // Close modal when clicking the × button
    closeButton.onclick = function() {
        modal.style.display = "none";
    }

    // Close modal when clicking outside of it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
