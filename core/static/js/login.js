document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.login-form');
    
    form.addEventListener('submit', function(event) {
        const username = document.getElementById('username');
        const password = document.getElementById('password');
        
        // Reset previous error states
        username.classList.remove('error');
        password.classList.remove('error');
        
        let isValid = true;
        
        // Validate username
        if (username.value.trim() === '') {
            isValid = false;
            username.classList.add('error');
        }
        
        // Validate password
        if (password.value.trim() === '') {
            isValid = false;
            password.classList.add('error');
        }
        
        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
            
            // Optional: Display an error message
            const errorContainer = document.createElement('div');
            errorContainer.classList.add('alert', 'alert-error');
            errorContainer.textContent = 'Please fill in all fields';
            
            // Insert error message before the form
            form.insertBefore(errorContainer, form.firstChild);
        }
    });
});