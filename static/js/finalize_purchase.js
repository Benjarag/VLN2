document.addEventListener('DOMContentLoaded', function() {
    // Get all radio buttons
    const paymentRadios = document.querySelectorAll('.payment-radio');
    
    // Get input fields for formatting - we'll set these IDs from the template
    const cardNumberInput = document.getElementById('card-number-input');
    const expiryInput = document.getElementById('expiry-input');
    const cvcInput = document.getElementById('cvc-input');
    
    // Function to show/hide fields based on selection
    function togglePaymentFields() {
        // Hide all payment fields first
        document.querySelectorAll('.payment-fields').forEach(field => {
            field.style.display = 'none';
        });
        
        // Find the checked radio button
        const checkedRadio = document.querySelector('input[name="payment_option"]:checked');
        
        if (checkedRadio) {
            const value = checkedRadio.value;
            
            // Show the corresponding fields
            if (value === 'Credit Card') {
                document.getElementById('credit-card-fields').style.display = 'block';
            } else if (value === 'Bank Transfer') {
                document.getElementById('bank-transfer-fields').style.display = 'block';
            } else if (value === 'Mortgage') {
                document.getElementById('mortgage-fields').style.display = 'block';
            }
        }
    }
    
    // Format credit card number with dashes after every 4 digits
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            // Get input value and remove any non-digit characters
            let value = this.value.replace(/\D/g, '');
            
            // Limit to 16 digits
            if (value.length > 16) {
                value = value.slice(0, 16);
            }
            
            // Format with dashes after every 4 digits
            let formattedValue = '';
            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formattedValue += '-';
                }
                formattedValue += value[i];
            }
            
            // Update input value
            this.value = formattedValue;
        });
    }
    
    // Format expiry date with slash after MM
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            // Get input value and remove any non-digit characters
            let value = this.value.replace(/\D/g, '');
            
            // Limit to 4 digits (MM/YY)
            if (value.length > 4) {
                value = value.slice(0, 4);
            }
            
            // Format with slash after first 2 digits
            if (value.length > 2) {
                value = value.slice(0, 2) + '/' + value.slice(2);
            }
            
            // Update input value
            this.value = value;
        });
    }
    
    // Limit CVC to 3 digits
    if (cvcInput) {
        cvcInput.addEventListener('input', function(e) {
            // Get input value and remove any non-digit characters
            let value = this.value.replace(/\D/g, '');
            
            // Limit to 3 digits
            if (value.length > 3) {
                value = value.slice(0, 3);
            }
            
            // Update input value
            this.value = value;
        });
    }
    
    // Add event listeners to all radio buttons
    paymentRadios.forEach(radio => {
        radio.addEventListener('change', togglePaymentFields);
    });
    
    // Initial toggle based on any pre-selected option
    togglePaymentFields();
});