// JavaScript to show/hide payment details based on selected option
document.addEventListener('DOMContentLoaded', function() {
    const paymentOptions = document.querySelectorAll('input[name="payment_option"]');
    const creditCardFields = document.getElementById('credit-card-fields');
    const bankTransferFields = document.getElementById('bank-transfer-fields');
    const mortgageFields = document.getElementById('mortgage-fields');

    if (!creditCardFields || !bankTransferFields || !mortgageFields) {
        return;
    }
    
    // Set proper maxlength for credit card input to account for formatting
    const creditCardNumberInput = document.getElementById('id_credit_card_number');
    if (creditCardNumberInput) {
        creditCardNumberInput.setAttribute('maxlength', '25'); // Increase maxlength to 25 to accommodate formatting
    }
    
    // Show appropriate fields based on initial selection
    showSelectedPaymentFields();

    // Add event listeners to radio buttons
    paymentOptions.forEach(option => {
        option.addEventListener('change', showSelectedPaymentFields);
    });

    function showSelectedPaymentFields() {
        // Hide all payment detail fields first
        creditCardFields.style.display = 'none';
        bankTransferFields.style.display = 'none';
        mortgageFields.style.display = 'none';

        // Show the relevant fields based on selection
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
    
    // Credit card formatting
    if (creditCardNumberInput) {
        creditCardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
            if (value.length > 16) value = value.substr(0, 16); // Limit to 16 digits
            
            // Add dashes after every 4 digits
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
    
    const creditCardExpiryInput = document.getElementById('id_credit_card_expiry');
    if (creditCardExpiryInput) {
        creditCardExpiryInput.setAttribute('maxlength', '5'); // MM/YY format needs 5 chars
        creditCardExpiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
            if (value.length > 4) value = value.substr(0, 4); // Limit to 4 digits
            
            // Add slash after first 2 digits
            if (value.length > 2) {
                e.target.value = value.substring(0, 2) + '/' + value.substring(2);
            } else {
                e.target.value = value;
            }
        });
    }
    
    const creditCardCvcInput = document.getElementById('id_credit_card_cvc');
    if (creditCardCvcInput) {
        creditCardCvcInput.setAttribute('maxlength', '3'); // CVC is 3 digits
        creditCardCvcInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
            if (value.length > 3) value = value.substr(0, 3); // Limit to 3 digits
            e.target.value = value;
        });
    }
});