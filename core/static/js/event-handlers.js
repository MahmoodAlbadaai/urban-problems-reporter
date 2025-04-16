document.addEventListener("DOMContentLoaded", function () {
    /*** ✅ Submit Event - Confirmation Before Submission ***/
    let forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function (event) {
            let confirmation = confirm("Are you sure you want to submit this form?");
            if (!confirmation) {
                event.preventDefault();
            }
        });
    });

    /*** ✅ Right Click Event - Disable Right Click on Sensitive Sections ***/
    let sensitiveSections = document.querySelectorAll(".form-container, .contact-form");
    sensitiveSections.forEach(section => {
        section.addEventListener("contextmenu", function (event) {
            alert("Right-click is disabled in this section for security reasons.");
            event.preventDefault();
        });
    });

    /*** ✅ Focus Event - Show Hint when Focusing on Input Fields ***/
    let inputFields = document.querySelectorAll("input, textarea");
    inputFields.forEach(input => {
        input.addEventListener("focus", function () {
            let hint = document.createElement("small");
            hint.textContent = "Tip: Please enter valid information.";
            hint.style.color = "blue";
            hint.classList.add("input-hint");
            this.parentNode.appendChild(hint);
        });

        input.addEventListener("blur", function () {
            let hints = this.parentNode.querySelectorAll(".input-hint");
            hints.forEach(hint => hint.remove());
        });
    });

    /*** ✅ Hover Event - Change Background on Hovering Buttons ***/
    let buttons = document.querySelectorAll("button");
    buttons.forEach(button => {
        button.addEventListener("mouseover", function () {
            this.style.backgroundColor = "#0056b3";
        });

        button.addEventListener("mouseout", function () {
            this.style.backgroundColor = "";
        });
    });
});
