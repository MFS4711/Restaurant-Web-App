// Get all "Add New" buttons
const addMenuItemButtons = document.querySelectorAll(".add-btn");

// Loop through all the "Add New" buttons and add click event listeners
addMenuItemButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault();

    // Get the category associated with this button (using the data-category attribute)
    const category = button.getAttribute("data-category");

    // Find the form associated with this category
    const form = document.querySelector(`.category-form[data-category="${category}"] .menu-item-form`);

    // Toggle the 'hidden' class to show or hide the form
    form.classList.toggle("hidden");
  });
});