// // JavaScript to show/hide payment details based on selected option
// document.addEventListener('DOMContentLoaded', function() {
//     const paymentOptions = document.querySelectorAll('input[name="payment_option"]');
//     const creditCardFields = document.getElementById('credit-card-fields');
//     const bankTransferFields = document.getElementById('bank-transfer-fields');
//     const mortgageFields = document.getElementById('mortgage-fields');
//
//     if (!creditCardFields || !bankTransferFields || !mortgageFields) {
//         return;
//     }
//
//     // Set proper maxlength for credit card input to account for formatting
//     const creditCardNumberInput = document.getElementById('id_credit_card_number');
//     if (creditCardNumberInput) {
//         creditCardNumberInput.setAttribute('maxlength', '25'); // Increase maxlength to 25 to accommodate formatting
//     }
//
//     // Show appropriate fields based on initial selection
//     showSelectedPaymentFields();
//
//     // Add event listeners to radio buttons
//     paymentOptions.forEach(option => {
//         option.addEventListener('change', showSelectedPaymentFields);
//     });
//
//     function showSelectedPaymentFields() {
//         // Hide all payment detail fields first
//         creditCardFields.style.display = 'none';
//         bankTransferFields.style.display = 'none';
//         mortgageFields.style.display = 'none';
//
//         // Show the relevant fields based on selection
//         const selectedOption = document.querySelector('input[name="payment_option"]:checked');
//         if (selectedOption) {
//             if (selectedOption.value === 'Credit Card') {
//                 creditCardFields.style.display = 'block';
//             } else if (selectedOption.value === 'Bank Transfer') {
//                 bankTransferFields.style.display = 'block';
//             } else if (selectedOption.value === 'Mortgage') {
//                 mortgageFields.style.display = 'block';
//             }
//         }
//     }
//
//     // Credit card formatting
//     if (creditCardNumberInput) {
//         creditCardNumberInput.addEventListener('input', function(e) {
//             let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
//             if (value.length > 16) value = value.substr(0, 16); // Limit to 16 digits
//
//             // Add dashes after every 4 digits
//             let formattedValue = '';
//             for (let i = 0; i < value.length; i++) {
//                 if (i > 0 && i % 4 === 0) {
//                     formattedValue += ' - ';
//                 }
//                 formattedValue += value[i];
//             }
//
//             e.target.value = formattedValue;
//         });
//     }
//
//     const creditCardExpiryInput = document.getElementById('id_credit_card_expiry');
//     if (creditCardExpiryInput) {
//         creditCardExpiryInput.setAttribute('maxlength', '5'); // MM/YY format needs 5 chars
//         creditCardExpiryInput.addEventListener('input', function(e) {
//             let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
//             if (value.length > 4) value = value.substr(0, 4); // Limit to 4 digits
//
//             // Add slash after first 2 digits
//             if (value.length > 2) {
//                 e.target.value = value.substring(0, 2) + '/' + value.substring(2);
//             } else {
//                 e.target.value = value;
//             }
//         });
//     }
//
//     const creditCardCvcInput = document.getElementById('id_credit_card_cvc');
//     if (creditCardCvcInput) {
//         creditCardCvcInput.setAttribute('maxlength', '3'); // CVC is 3 digits
//         creditCardCvcInput.addEventListener('input', function(e) {
//             let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
//             if (value.length > 3) value = value.substr(0, 3); // Limit to 3 digits
//             e.target.value = value;
//         });
//     }
// });


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
