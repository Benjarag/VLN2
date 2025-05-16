document.addEventListener('DOMContentLoaded', function() {
    // Get all form elements
    const cardNumberInput = document.querySelector('input[name="credit_card_number"]');
    const expiryInput = document.querySelector('input[name="credit_card_expiry"]');
    const cvcInput = document.querySelector('input[name="credit_card_cvc"]');
    const paymentOptions = document.querySelectorAll('input[name="payment_option"]');

    // Credit Card Number Formatting
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            // Remove any non-digit characters
            let value = this.value.replace(/\D/g, '');

            // Limit to 16 digits
            if (value.length > 16) {
                value = value.slice(0, 16);
            }

            // Add dashes after every 4 digits
            let formattedValue = '';
            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formattedValue += '-';
                }
                formattedValue += value[i];
            }

            // Update the input value
            this.value = formattedValue;
        });
    }

    // Credit Card Expiry Formatting
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            // Remove any non-digit characters except /
            let value = this.value.replace(/[^\d\/]/g, '');

            // Remove any existing slashes
            value = value.replace(/\//g, '');

            // Limit to 4 digits (MM/YY)
            if (value.length > 4) {
                value = value.slice(0, 4);
            }

            // Add slash after 2 digits
            if (value.length > 2) {
                value = value.slice(0, 2) + '/' + value.slice(2);
            }

            // Update the input value
            this.value = value;
        });
    }

    // CVC Formatting - exactly 3 digits
    if (cvcInput) {
        cvcInput.addEventListener('input', function(e) {
            // Only allow digits
            let value = this.value.replace(/\D/g, '');

            // Limit to 3 digits
            if (value.length > 3) {
                value = value.slice(0, 3);
            }

            // Update the input value
            this.value = value;
        });
    }

    // Show/hide payment specific fields based on selected payment option
    function togglePaymentFields() {
        const selectedOption = document.querySelector('input[name="payment_option"]:checked');

        const creditCardFields = document.querySelectorAll('.credit-card-fields');
        const bankFields = document.querySelectorAll('.bank-fields');
        const mortgageFields = document.querySelectorAll('.mortgage-fields');

        // Hide all fields initially
        creditCardFields.forEach(field => field.style.display = 'none');
        bankFields.forEach(field => field.style.display = 'none');
        mortgageFields.forEach(field => field.style.display = 'none');

        // Show relevant fields based on selection
        if (selectedOption) {
            if (selectedOption.value === 'Credit Card') {
                creditCardFields.forEach(field => field.style.display = 'block');
            } else if (selectedOption.value === 'Bank Transfer') {
                bankFields.forEach(field => field.style.display = 'block');
            } else if (selectedOption.value === 'Mortgage') {
                mortgageFields.forEach(field => field.style.display = 'block');
            }
        }
    }

    // Set up event listeners for payment option changes
    paymentOptions.forEach(option => {
        option.addEventListener('change', togglePaymentFields);
    });

    // Initialize fields on page load
    togglePaymentFields();
});