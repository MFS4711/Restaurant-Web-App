// Get all "Add New" buttons
const addMenuItemButtons = document.querySelectorAll(".add-btn");

// Loop through all the "Add New" buttons and add click event listeners
addMenuItemButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault();

    // Get the category associated with this button (using the data-category attribute)
    const category = button.getAttribute("data-category");

    // Find the form associated with this category
    const form = document.querySelector(
      `.category-form[data-category="${category}"] .menu-item-form`
    );

    // Toggle the 'hidden' class to show or hide the form
    form.classList.toggle("hidden");
  });
});

// Get all "Edit" buttons
const editButtons = document.querySelectorAll(".edit-btn");

// Loop through all the "Edit" buttons and add click event listeners
editButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault();

    // Get the menu item ID from the button (stored in data-menu-item-id)
    const menuItemId = e.target.getAttribute("data-menu-item-id");

    // Retrieve the data for this menu item
    const menuItemNameValue = document.getElementById(`menu-item-name-${menuItemId}`).innerText;
    const menuItemDescriptionValue = document.getElementById(`menu-item-description-${menuItemId}`).innerText;
    const menuItemPriceValue = document.getElementById(`menu-item-price-${menuItemId}`).innerText;
    const menuItemIsAvailableValue = document.getElementById(`menu-item-is-available-${menuItemId}`).innerText;

    // Find the specific form fields for this menu item
    const editForm = document.getElementById(`edit-form-${menuItemId}`);
    const menuItemNameInput = editForm.querySelector("input[name='name']");
    const menuItemDescriptionInput = editForm.querySelector("textarea[name='description']");
    const menuItemPriceInput = editForm.querySelector("input[name='price']");
    const menuItemIsAvailableInput = editForm.querySelector("input[name='is_available']");

    // Populate the form fields with the current values
    menuItemNameInput.value = menuItemNameValue;
    menuItemDescriptionInput.value = menuItemDescriptionValue;
    menuItemPriceInput.value = menuItemPriceValue;
    menuItemIsAvailableInput.value = menuItemIsAvailableValue;

    // Toggle the 'hidden' class to show or hide the form
    const form = editForm.querySelector(".menu-item-form");
    form.classList.toggle("hidden");
  });
});


// JS for bootstrap Modal:
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
// Delete buttons
const deleteButtons = document.getElementsByClassName("delete-btn");
const deleteConfirm = document.getElementById("delete-confirm");

/**
 * Initializes deletion functionality for the provided delete buttons.
 *
 * For each button in the `deleteButtons` collection:
 * - Retrieves the associated menu item's ID upon click.
 * - Updates the `deleteConfirm` link's href to point to the
 *   deletion endpoint for the specific menu item.
 * - Displays a confirmation modal (`deleteModal`) to prompt
 *   the user for confirmation before deletion.
 */
for (let button of deleteButtons) {
  button.addEventListener("click", (e) => {
    let menuItemId = e.target.getAttribute("data-menu-item-id"); // Get the menu item ID
    deleteConfirm.href = `/menu/delete-menu-item/${menuItemId}`; // Adjust URL to match the Django URL pattern
    deleteModal.show(); // Show the confirmation modal
  });
}