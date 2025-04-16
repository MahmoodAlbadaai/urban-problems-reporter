document.addEventListener("DOMContentLoaded", function () {
    let form = document.getElementById("contactForm");
    let tableBody = document.querySelector("#messagesTable tbody");
    let showMessagesButton = document.getElementById("show-messages");
    let clearMessagesButton = document.getElementById("clear-messages");

    // Load stored messages when the page loads
    displayMessages();

    // Handle form submission
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let name = document.getElementById("contact-name").value.trim();
        let email = document.getElementById("contact-email").value.trim();
        let message = document.getElementById("contact-message").value.trim();

        let isValid = true;
        document.querySelectorAll(".error-message").forEach(e => e.style.display = "none");

        if (name.length < 3) {
            document.getElementById("contact-name-error").textContent = "Name must be at least 3 characters.";
            document.getElementById("contact-name-error").style.display = "block";
            isValid = false;
        }

        if (!email.includes("@") || email.length < 5) {
            document.getElementById("contact-email-error").textContent = "Enter a valid email.";
            document.getElementById("contact-email-error").style.display = "block";
            isValid = false;
        }

        if (message.length < 10) {
            document.getElementById("contact-message-error").textContent = "Message must be at least 10 characters.";
            document.getElementById("contact-message-error").style.display = "block";
            isValid = false;
        }

        if (!isValid) return;

        let messages = JSON.parse(localStorage.getItem("messages")) || [];

        // Add new message to array
        messages.push({
            name,
            email,
            message
        });

        // Store updated messages in LocalStorage
        localStorage.setItem("messages", JSON.stringify(messages));

        // Refresh the table with new data
        displayMessages();

        // Clear the form fields after submission
        form.reset();
    });

    // Function to display messages in table
    function displayMessages() {
        let messages = JSON.parse(localStorage.getItem("messages")) || [];
        tableBody.innerHTML = "";

        messages.forEach((msg, index) => {
            let row = `
                <tr>
                    <td>${msg.name}</td>
                    <td>${msg.email}</td>
                    <td>${msg.message}</td>
                    <td><button class="delete-btn" onclick="deleteMessage(${index})">❌</button></td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    // Delete a specific message from the table
    window.deleteMessage = function (index) {
        let messages = JSON.parse(localStorage.getItem("messages")) || [];
        messages.splice(index, 1); // Remove the selected message
        localStorage.setItem("messages", JSON.stringify(messages));
        displayMessages(); // Refresh the table
    };

    // Show stored messages when button is clicked
    showMessagesButton.addEventListener("click", displayMessages);

    // Clear all messages when button is clicked
    clearMessagesButton.addEventListener("click", function () {
        localStorage.removeItem("messages");
        displayMessages(); // Refresh the table
    });
});
