
// Function to format a number with thousands separators (2000 -> 2.000)
function formatNumber(n) {
    // Ensure the input is a string
    if (typeof n !== 'string') return '';
    // Remove existing dots before re-formatting (to handle editing)
    let cleaned = n.replace(/\./g, '');
    // Format with dots every three digits
    return cleaned.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

document.querySelectorAll('.js-localize-input').forEach(input => {
    // Format on input
    input.addEventListener('input', function() {
        // Store the cursor position
        let start = this.selectionStart;
        let end = this.selectionEnd;

        const originalValue = this.value;
        const formattedValue = formatNumber(originalValue);
        
        this.value = formattedValue;
    });

    // Format on page load (for pre-filled values)
    input.value = formatNumber(input.value);

    // 3. Update the clean hidden field before form submission
    const form = input.closest('form');
    const cleanInputId = input.id
    // .replace('_display', '_clean');
    const cleanInput = document.getElementById(cleanInputId);
    
    // Remove all dots from the displayed value before submission
    form.addEventListener('submit', function() {
        
        const cleanValue = input.value.replace(/\./g, '');
        cleanInput.value = cleanValue; 
    });
});
