document.addEventListener("DOMContentLoaded", function () {
    // Validate Report an Issue Form
    let issueForm = document.getElementById("issueForm");
    if (issueForm) {
        issueForm.addEventListener("submit", function (event) {
            let isValid = true;

            let issueType = document.getElementById("issue-type");
            let location = document.getElementById("location");
            let description = document.getElementById("description");
            let email = document.getElementById("email");
            let phone = document.getElementById("phone");

            document.querySelectorAll(".error-message").forEach(e => e.style.display = "none");

            if (issueType.value === "") {
                document.getElementById("issue-error").textContent = "Please select an issue type.";
                document.getElementById("issue-error").style.display = "block";
                isValid = false;
            }

            if (location.value.trim().length < 5) {
                document.getElementById("location-error").textContent = "Location must be at least 5 characters long.";
                document.getElementById("location-error").style.display = "block";
                isValid = false;
            }

            if (description.value.trim().length < 10) {
                document.getElementById("description-error").textContent = "Description must be at least 10 characters.";
                document.getElementById("description-error").style.display = "block";
                isValid = false;
            }

            let phonePattern = /^[0-9]{10}$/;
            if (phone.value !== "" && !phonePattern.test(phone.value)) {
                document.getElementById("phone-error").textContent = "Enter a valid 10-digit phone number.";
                document.getElementById("phone-error").style.display = "block";
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }

    // Validate Contact Form
    let contactForm = document.getElementById("contactForm");
    if (contactForm) {
        contactForm.addEventListener("submit", function (event) {
            let isValid = true;

            let name = document.getElementById("contact-name");
            let email = document.getElementById("contact-email");
            let message = document.getElementById("contact-message");

            if (name.value.trim().length < 3) {
                document.getElementById("contact-name-error").textContent = "Name must be at least 3 characters.";
                document.getElementById("contact-name-error").style.display = "block";
                isValid = false;
            }

            if (email.value.trim() === "" || !email.value.includes("@")) {
                document.getElementById("contact-email-error").textContent = "Enter a valid email.";
                document.getElementById("contact-email-error").style.display = "block";
                isValid = false;
            }

            if (message.value.trim().length < 10) {
                document.getElementById("contact-message-error").textContent = "Message must be at least 10 characters.";
                document.getElementById("contact-message-error").style.display = "block";
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }

    // Validate Login Form
    let loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            let isValid = true;

            let username = document.getElementById("username");
            let password = document.getElementById("password");

            if (username.value.trim().length < 4) {
                document.getElementById("username-error").textContent = "Username must be at least 4 characters.";
                document.getElementById("username-error").style.display = "block";
                isValid = false;
            }

            if (password.value.trim().length < 6) {
                document.getElementById("password-error").textContent = "Password must be at least 6 characters.";
                document.getElementById("password-error").style.display = "block";
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }

    // Validate Registration Form
    let registrationForm = document.getElementById("registrationForm");
    if (registrationForm) {
        registrationForm.addEventListener("submit", function (event) {
            let isValid = true;

            let username = document.getElementById("username");
            let password = document.getElementById("password");
            let confirmPassword = document.getElementById("confirm-password");
            let gender = document.querySelector('input[name="gender"]:checked');
            let terms = document.getElementById("terms");

            if (username.value.trim().length < 4) {
                document.getElementById("username-error").textContent = "Username must be at least 4 characters.";
                document.getElementById("username-error").style.display = "block";
                isValid = false;
            }

            if (password.value.trim().length < 6) {
                document.getElementById("password-error").textContent = "Password must be at least 6 characters.";
                document.getElementById("password-error").style.display = "block";
                isValid = false;
            }

            if (confirmPassword.value !== password.value) {
                document.getElementById("confirm-password-error").textContent = "Passwords do not match.";
                document.getElementById("confirm-password-error").style.display = "block";
                isValid = false;
            }

            if (!gender) {
                document.getElementById("gender-error").textContent = "Please select a gender.";
                document.getElementById("gender-error").style.display = "block";
                isValid = false;
            }

            if (!terms.checked) {
                document.getElementById("terms-error").textContent = "You must agree to the Terms & Conditions.";
                document.getElementById("terms-error").style.display = "block";
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }
});
