document.addEventListener("DOMContentLoaded", function () {
    let form = document.getElementById("registrationForm");
    let tableBody = document.querySelector("#usersTable tbody");
    let showUsersButton = document.getElementById("show-users");
    let clearUsersButton = document.getElementById("clear-users");

    // Load stored users when the page loads
    displayUsers();

    // Handle form submission
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let username = document.getElementById("username").value.trim();
        let password = document.getElementById("password").value.trim();
        let confirmPassword = document.getElementById("confirm-password").value.trim();
        let gender = document.querySelector('input[name="gender"]:checked');
        let terms = document.getElementById("terms");

        let isValid = true;
        document.querySelectorAll(".error-message").forEach(e => e.style.display = "none");

        if (username.length < 4) {
            document.getElementById("username-error").textContent = "Username must be at least 4 characters.";
            document.getElementById("username-error").style.display = "block";
            isValid = false;
        }

        if (password.length < 6) {
            document.getElementById("password-error").textContent = "Password must be at least 6 characters.";
            document.getElementById("password-error").style.display = "block";
            isValid = false;
        }

        if (confirmPassword !== password) {
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

        if (!isValid) return;

        let users = JSON.parse(localStorage.getItem("users")) || [];

        // Add new user to array
        users.push({
            username,
            gender: gender.value
        });

        // Store updated users in LocalStorage
        localStorage.setItem("users", JSON.stringify(users));

        // Refresh the table with new data
        displayUsers();

        // Clear the form fields after submission
        form.reset();
    });

    // Function to display users in table
    function displayUsers() {
        let users = JSON.parse(localStorage.getItem("users")) || [];
        tableBody.innerHTML = "";

        users.forEach((user, index) => {
            let row = `
                <tr>
                    <td>${user.username}</td>
                    <td>${user.gender}</td>
                    <td><button class="delete-btn" onclick="deleteUser(${index})">❌</button></td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    // Delete a specific user from the table
    window.deleteUser = function (index) {
        let users = JSON.parse(localStorage.getItem("users")) || [];
        users.splice(index, 1); // Remove the selected user
        localStorage.setItem("users", JSON.stringify(users));
        displayUsers(); // Refresh the table
    };

    // Show stored users when button is clicked
    showUsersButton.addEventListener("click", displayUsers);

    // Clear all users when button is clicked
    clearUsersButton.addEventListener("click", function () {
        localStorage.removeItem("users");
        displayUsers(); // Refresh the table
    });
});
