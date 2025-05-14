
// JavaScript to show/hide payment details based on selected option
document.addEventListener('DOMContentLoaded', function() {
    const paymentOptions = document.querySelectorAll('input[name="payment_option"]');
    const creditCardFields = document.getElementById('credit-card-fields');
    const bankTransferFields = document.getElementById('bank-transfer-fields');
    const mortgageFields = document.getElementById('mortgage-fields');

    if (!creditCardFields || !bankTransferFields || !mortgageFields) {
        return;
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
});
