// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function () {
    let menuButton = document.getElementById("menu-toggle");
    let navMenu = document.getElementById("nav-menu");
    let closeButton = document.getElementById("close-menu");

    // Toggle the slide-in menu on button click
    menuButton.addEventListener("click", function () {
        navMenu.classList.toggle("show-menu"); // Slide menu in and out
    });

    // Close the menu when clicking outside it
    document.addEventListener("click", function (event) {
        if (!menuButton.contains(event.target) && !navMenu.contains(event.target) && !closeButton.contains(event.target)) {
            navMenu.classList.remove("show-menu"); // Hide menu if clicked outside
        }
    });

    // Close menu when clicking the "✖ Close" button
    closeButton.addEventListener("click", function () {
        navMenu.classList.remove("show-menu"); // Close menu
    });
});
