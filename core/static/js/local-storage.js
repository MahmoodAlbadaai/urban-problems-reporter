document.addEventListener("DOMContentLoaded", function () {
    let form = document.getElementById("issueForm");
    let tableBody = document.querySelector("#reportsTable tbody");
    let showReportsButton = document.getElementById("show-reports");
    let clearReportsButton = document.getElementById("clear-reports");

    // Load stored reports when the page loads
    displayReports();

    // Handle form submission
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let issueType = document.getElementById("issue-type").value;
        let location = document.getElementById("location").value;
        let description = document.getElementById("description").value;
        let email = document.getElementById("email").value;
        let phone = document.getElementById("phone").value;
        let date = document.getElementById("date").value;

        let reports = JSON.parse(localStorage.getItem("reports")) || [];

        // Add new report to array
        reports.push({
            issueType,
            location,
            description,
            email,
            phone,
            date
        });

        // Store updated reports in LocalStorage
        localStorage.setItem("reports", JSON.stringify(reports));

        // Refresh the table with new data
        displayReports();

        // Clear the form fields after submission
        form.reset();
    });

    // Function to display reports in table
    function displayReports() {
        let reports = JSON.parse(localStorage.getItem("reports")) || [];
        tableBody.innerHTML = "";

        reports.forEach((report, index) => {
            let row = `
                <tr>
                    <td>${report.issueType}</td>
                    <td>${report.location}</td>
                    <td>${report.description}</td>
                    <td>${report.email}</td>
                    <td>${report.phone}</td>
                    <td>${report.date}</td>
                    <td><button class="delete-btn" onclick="deleteReport(${index})">❌</button></td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    // Delete a specific report from the table
    window.deleteReport = function (index) {
        let reports = JSON.parse(localStorage.getItem("reports")) || [];
        reports.splice(index, 1); // Remove the selected report
        localStorage.setItem("reports", JSON.stringify(reports));
        displayReports(); // Refresh the table
    };

    // Show stored reports when button is clicked
    showReportsButton.addEventListener("click", displayReports);

    // Clear all reports when button is clicked
    clearReportsButton.addEventListener("click", function () {
        localStorage.removeItem("reports");
        displayReports(); // Refresh the table
    });
});
