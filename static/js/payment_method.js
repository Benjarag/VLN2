document.addEventListener('DOMContentLoaded', function() {
    // Show relevant payment fields on page load
    const paymentOptions = document.querySelectorAll('input[name="payment_option"]');
    const creditCardFields = document.getElementById('credit-card-fields');
    const bankTransferFields = document.getElementById('bank-transfer-fields');
    const mortgageFields = document.getElementById('mortgage-fields');

    // Function to show the appropriate payment fields
    function showPaymentFields() {
        // Hide all payment fields first
        creditCardFields.style.display = 'none';
        bankTransferFields.style.display = 'none';
        mortgageFields.style.display = 'none';

        // Show relevant fields based on selected option
        const selectedOption = document.querySelector('input[name="payment_option"]:checked');
        if (selectedOption) {
            if (selectedOption.value === 'Credit Card') {
                creditCardFields.style.display = 'block';
            } else if (selectedOption.value === 'Bank Transfer') {
                bankTransferFields.style.display = 'block';
            } else if (selectedOption.value === 'Mortgage') {
                mortgageFields.style.display = 'block';
            }
        }
    }

    // Initialize on page load
    showPaymentFields();

    // Update fields when payment option changes
    paymentOptions.forEach(option => {
        option.addEventListener('change', showPaymentFields);
    });

    // Format CVC to ensure it's only 3 digits
    const cvcInput = document.querySelector('input[name="credit_card_cvc"]');
    if (cvcInput) {
        cvcInput.setAttribute('maxlength', '3');
        cvcInput.addEventListener('input', function(e) {
            // Remove any non-digits
            let value = e.target.value.replace(/\D/g, '');
            // Limit to 3 digits
            if (value.length > 3) {
                value = value.substring(0, 3);
            }
            e.target.value = value;
        });
    }

    // Format credit card number with spaces
    const ccNumberInput = document.querySelector('input[name="credit_card_number"]');
    if (ccNumberInput) {
        ccNumberInput.addEventListener('input', function(e) {
            // Remove non-digits
            let value = e.target.value.replace(/\D/g, '');
            // Limit to 16 digits
            if (value.length > 16) {
                value = value.substring(0, 16);
            }

            // Add spaces after every 4 digits
            let formattedValue = '';
            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formattedValue += ' - ';
                }
                formattedValue += value[i];
            }

            e.target.value = formattedValue;
        });
    }

    // Format expiry date
    const expiryInput = document.querySelector('input[name="credit_card_expiry"]');
    if (expiryInput) {
        expiryInput.setAttribute('maxlength', '5');
        expiryInput.addEventListener('input', function(e) {
            // Remove non-digits
            let value = e.target.value.replace(/\D/g, '');
            // Limit to 4 digits
            if (value.length > 4) {
                value = value.substring(0, 4);
            }

            // Add slash after first 2 digits
            if (value.length > 2) {
                e.target.value = value.substring(0, 2) + '/' + value.substring(2);
            } else {
                e.target.value = value;
            }
        });
    }
});