
document.addEventListener('DOMContentLoaded', function() {
    // Get all payment option radio buttons
    const paymentOptions = document.querySelectorAll('input[name="payment_option"]');
    const creditCardFields = document.getElementById('credit-card-fields');
    const bankTransferFields = document.getElementById('bank-transfer-fields');
    const mortgageFields = document.getElementById('mortgage-fields');
    const submitButton = document.querySelector('.submit-button');

    // Function to show the relevant payment fields
    function showPaymentFields() {
        // Hide all payment fields first
        creditCardFields.style.display = 'none';
        bankTransferFields.style.display = 'none';
        mortgageFields.style.display = 'none';

        // Show the relevant fields based on selected payment option
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

    // Add event listeners to payment options
    paymentOptions.forEach(option => {
        option.addEventListener('change', showPaymentFields);
    });

    // Initial call to set up the form correctly
    showPaymentFields();

    // Form submission validation
    document.querySelector('form').addEventListener('submit', function(e) {
        const selectedOption = document.querySelector('input[name="payment_option"]:checked');
        let isValid = true;

        if (selectedOption) {
            if (selectedOption.value === 'Credit Card') {
                // Validate credit card fields
                const cardholderName = document.querySelector('input[name="cardholder_name"]').value;
                const cardNumber = document.querySelector('input[name="credit_card_number"]').value;
                const expiry = document.querySelector('input[name="credit_card_expiry"]').value;
                const cvc = document.querySelector('input[name="credit_card_cvc"]').value;

                if (!cardholderName || !cardNumber || !expiry || !cvc) {
                    alert('Please fill in all credit card information');
                    isValid = false;
                }
            } else if (selectedOption.value === 'Bank Transfer') {
                // Validate bank transfer fields
                const bankAccount = document.querySelector('input[name="bank_account"]').value;

                if (!bankAccount) {
                    alert('Please enter your bank account information');
                    isValid = false;
                }
            } else if (selectedOption.value === 'Mortgage') {
                // Validate mortgage fields
                const mortgageProvider = document.querySelector('select[name="mortgage_provider"]').value;

                if (!mortgageProvider) {
                    alert('Please select a mortgage provider');
                    isValid = false;
                }
            }
        } else {
            alert('Please select a payment option');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault(); // Prevent form submission if validation fails
        }
    });
});
