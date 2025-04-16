document.addEventListener('DOMContentLoaded', function() {
    /**
     * Main form validation for issue reporting
     * Validates all required fields and displays appropriate error messages
     */
    const form = document.getElementById('issueForm');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Reset all error messages from previous validation attempts
            document.querySelectorAll('.error-message').forEach(el => {
                el.style.display = 'none';
            });
            
            // Get references to all form fields
            const issueTypeField = document.getElementById(form.elements['issue_type'].id);
            const locationField = document.getElementById(form.elements['location'].id);
            const titleField = document.getElementById(form.elements['title'].id);
            const descriptionField = document.getElementById(form.elements['description'].id);
            const reporterNameField = document.getElementById(form.elements['reporter_name'].id);
            const reporterEmailField = document.getElementById(form.elements['reporter_email'].id);
            const reporterPhoneField = document.getElementById(form.elements['reporter_phone'].id);
            const incidentDateField = document.getElementById(form.elements['incident_date'].id);
            
            // Validate Issue Type: must be selected
            if (!issueTypeField.value) {
                document.getElementById('issue-type-error').textContent = 'Please select an issue type.';
                document.getElementById('issue-type-error').style.display = 'block';
                isValid = false;
            }
            
            // Validate Location: must be selected
            if (!locationField.value) {
                document.getElementById('location-error').textContent = 'Please select a location.';
                document.getElementById('location-error').style.display = 'block';
                isValid = false;
            }
            
            // Validate Title: minimum 5 characters
            if (titleField.value.trim().length < 5) {
                document.getElementById('title-error').textContent = 'Title must be at least 5 characters long.';
                document.getElementById('title-error').style.display = 'block';
                isValid = false;
            }
            
            // Validate Description: minimum 10 characters
            if (descriptionField.value.trim().length < 10) {
                document.getElementById('description-error').textContent = 'Description must be at least 10 characters long.';
                document.getElementById('description-error').style.display = 'block';
                isValid = false;
            }
            
            // Validate Reporter Name: minimum 3 characters
            if (reporterNameField.value.trim().length < 3) {
                document.getElementById('reporter-name-error').textContent = 'Name must be at least 3 characters long.';
                document.getElementById('reporter-name-error').style.display = 'block';
                isValid = false;
            }
            
            // Validate Reporter Email: must contain @ and be at least 5 characters
            if (!reporterEmailField.value.includes('@') || reporterEmailField.value.trim().length < 5) {
                document.getElementById('reporter-email-error').textContent = 'Please enter a valid email address.';
                document.getElementById('reporter-email-error').style.display = 'block';
                isValid = false;
            }
            
            // Validate Phone (optional field): must match valid phone pattern if provided
            if (reporterPhoneField.value.trim() !== '') {
                const phonePattern = /^\+?[0-9]{10,15}$/;
                if (!phonePattern.test(reporterPhoneField.value.trim())) {
                    document.getElementById('reporter-phone-error').textContent = 'Please enter a valid phone number (10-15 digits).';
                    document.getElementById('reporter-phone-error').style.display = 'block';
                    isValid = false;
                }
            }
            
            // Validate Incident Date: must be provided and not in the future
            if (!incidentDateField.value) {
                document.getElementById('incident-date-error').textContent = 'Please select the date of the incident.';
                document.getElementById('incident-date-error').style.display = 'block';
                isValid = false;
            } else {
                const selectedDate = new Date(incidentDateField.value);
                const today = new Date();
                if (selectedDate > today) {
                    document.getElementById('incident-date-error').textContent = 'Incident date cannot be in the future.';
                    document.getElementById('incident-date-error').style.display = 'block';
                    isValid = false;
                }
            }
            
            // Prevent form submission if validation fails
            if (!isValid) {
                event.preventDefault();
                // Scroll to the first error for better user experience
                const firstError = document.querySelector('.error-message[style="display: block;"]');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            } else {
                console.log("Form is being submitted...");
            }
        });
    } else {
        console.error("Form element with ID 'issueForm' not found");
    }
    
    /**
     * Location modal functionality
     * Allows users to add a new location via AJAX without leaving the page
     */
    const modal = document.getElementById('location-modal');
    const addLocationBtn = document.getElementById('add-location-btn');
    
    // Check if modal elements exist
    if (!modal || !addLocationBtn) {
        console.error("Modal or Add Location button not found");
        return;
    }
    
    const closeBtn = modal.querySelector('.close');
    const locationForm = document.getElementById('location-form');
    const locationSelect = document.getElementById(form.elements['location'].id);
    
    // Show modal when "Add New Location" button is clicked
    addLocationBtn.addEventListener('click', function() {
        modal.style.display = 'block';
    });
    
    // Close modal when "X" button is clicked
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    // Close modal when clicking outside of modal content
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Location form submission handling
    if (locationForm && locationSelect) {
        locationForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Get form field elements
            const nameInput = document.getElementById('location-name');
            const addressInput = document.getElementById('location-address');
            const latInput = document.getElementById('location-latitude');
            const lngInput = document.getElementById('location-longitude');
            const errorsDiv = document.getElementById('location-errors');
            
            // Check if all elements exist
            if (!nameInput || !addressInput || !latInput || !lngInput || !errorsDiv) {
                console.error("One or more form inputs not found");
                return;
            }
            
            // Client-side validation
            let isValid = true;
            let errors = [];
            
            // Validate location name
            if (nameInput.value.trim() === '') {
                errors.push('Location name is required');
                isValid = false;
            }
            
            // Validate either address or coordinates are provided
            if (addressInput.value.trim() === '' && (!latInput.value || !lngInput.value)) {
                errors.push('Either address or both latitude and longitude are required');
                isValid = false;
            }
            
            // If validation fails, display errors and stop form submission
            if (!isValid) {
                errorsDiv.innerHTML = errors.map(e => `<p>${e}</p>`).join('');
                errorsDiv.style.display = 'block';
                return;
            }
            
            // Reset errors if validation passes
            errorsDiv.style.display = 'none';
            
            // Prepare form data for AJAX request
            const formData = new FormData();
            formData.append('name', nameInput.value);
            formData.append('address', addressInput.value);
            if (latInput.value) formData.append('latitude', latInput.value);
            if (lngInput.value) formData.append('longitude', lngInput.value);
            formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
            
            // Send AJAX request to add location
            fetch('/ajax/add-location/', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Add the new location to the dropdown
                    const option = document.createElement('option');
                    option.value = data.location_id;
                    option.textContent = data.location_name;
                    locationSelect.appendChild(option);
                    
                    // Select the new location
                    locationSelect.value = data.location_id;
                    
                    // Close the modal
                    modal.style.display = 'none';
                    
                    // Reset the form
                    locationForm.reset();
                } else {
                    // Display server-side errors
                    errorsDiv.innerHTML = '';
                    for (const field in data.errors) {
                        const error = JSON.parse(data.errors)[field];
                        errorsDiv.innerHTML += `<p>${error.join(' ')}</p>`;
                    }
                    errorsDiv.style.display = 'block';
                }
            })
            .catch(error => {
                // Handle AJAX errors
                console.error('Error:', error);
                errorsDiv.innerHTML = '<p>An error occurred. Please try again.</p>';
                errorsDiv.style.display = 'block';
            });
        });
    } else {
        console.error("Location form or select element not found");
    }
});