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
    const menuItemNameValue = document.getElementById(
      `menu-item-name-${menuItemId}`
    ).innerText;
    const menuItemDescriptionValue = document.getElementById(
      `menu-item-description-${menuItemId}`
    ).innerText;
    const menuItemPriceValue = document.getElementById(
      `menu-item-price-${menuItemId}`
    ).innerText;
    const menuItemIsAvailableValue = document.getElementById(
      `menu-item-is-available-${menuItemId}`
    ).innerText;

    // Find the specific form fields for this menu item
    const editForm = document.getElementById(`edit-form-${menuItemId}`);
    const menuItemNameInput = editForm.querySelector("input[name='name']");
    const menuItemDescriptionInput = editForm.querySelector(
      "textarea[name='description']"
    );
    const menuItemPriceInput = editForm.querySelector("input[name='price']");
    const menuItemIsAvailableInput = editForm.querySelector(
      "input[name='is_available']"
    );

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

// Function to handle image preview
function handleImagePreview(input) {
  const file = input.files[0]; // Get the file from the input field
  const previewImage = document.getElementById("image-preview"); // Get the preview image element

  // Check if a file is selected
  if (file) {
    const reader = new FileReader(); // Create a FileReader to read the file

    reader.onload = function (e) {
      // Set the src of the preview image to the file's URL
      previewImage.src = e.target.result;
      previewImage.classList.remove("hidden"); // Show the preview image
    };

    reader.readAsDataURL(file); // Read the image as a data URL
  } else {
    previewImage.classList.add("hidden"); // Hide the preview if no file is selected
  }
}

// Add event listener to the image input field in the form
const imageInput = document.querySelector("input[name='image']"); // Get the file input field

if (imageInput) {
  imageInput.addEventListener("change", function () {
    handleImagePreview(this); // Call the function to update the image preview
  });
}

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

// Modal to view menu item details
// Get all menu item titles that will trigger the modal
const menuItemTitles = document.querySelectorAll('.menu-item-title');

// Loop through all menu item titles and add click event listeners
menuItemTitles.forEach((title) => {
    title.addEventListener('click', (e) => {
        const menuItemId = e.target.getAttribute('data-bs-target').split('-')[1]; // Extract menu item ID from the modal target

        // Get the menu item data
        const menuItemName = document.getElementById(`menu-item-name-${menuItemId}`).innerText;
        const menuItemDescription = document.getElementById(`menu-item-description-${menuItemId}`).innerText;
        const menuItemPrice = document.getElementById(`menu-item-price-${menuItemId}`).innerText;
        const menuItemIsAvailable = document.getElementById(`menu-item-is-available-${menuItemId}`).innerText;

        // Update the modal content dynamically
        const modal = document.getElementById(`menuItemModal-${menuItemId}`);
        const modalTitle = modal.querySelector('.modal-title');
        const modalBody = modal.querySelector('.modal-body');
        const modalFooter = modal.querySelector('.modal-footer');

        modalTitle.innerText = menuItemName;
        modalBody.innerHTML = `
            <img src="${document.getElementById(`menu-item-image-${menuItemId}`).src}" alt="${menuItemName}" class="img-fluid">
            <h5>Description:</h5>
            <p>${menuItemDescription}</p>
            <h5>Price:</h5>
            <p>£${menuItemPrice}</p>
            <h5>Available:</h5>
            <p>${menuItemIsAvailable === 'True' ? 'Yes' : 'No'}</p>
        `;
    });
});