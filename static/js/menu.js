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

// form field data
const menuItemName = document.getElementById("id_name");
const menuItemDescription = document.getElementById("id_description");
const menuItemImage = document.getElementById("id_image");
const menuItemPrice = document.getElementById("id_price");
const menuItemIsAvailable = document.getElementById("id_is_available");

// Loop through all the "Edit" buttons and add click event listeners
editButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault();

    // Get the menu item ID from the button (stored in data-menu-item-id)
    const menuItemId = e.target.getAttribute("data-menu-item-id");

    // Retrieve the data
    const menuItemNameValue = document.getElementById(`menu-item-name-${menuItemId}`).innerText;
    // console.log(menuItemNameValue);
    const menuItemDescriptionValue = document.getElementById(`menu-item-description-${menuItemId}`).innerText;
    // const menuItemImageValue = document.getElementById(`menu-item-image-${menuItemId}`).innerText;
    const menuItemPriceValue = document.getElementById(`menu-item-price-${menuItemId}`).innerText;
    const menuItemIsAvailableValue = document.getElementById(`menu-item-is-available-${menuItemId}`).innerText;

    // populate form fields
    menuItemName.value = menuItemNameValue;
    menuItemDescription.value = menuItemDescriptionValue;
    // menuItemImage.value = menuItemImageValue;
    menuItemPrice.value = menuItemPriceValue;
    menuItemIsAvailable.value = menuItemIsAvailableValue;

    // Find the form associated with this menu item
    const editForm = document.getElementById(`edit-form-${menuItemId}`);

    // Find the form element inside the row and toggle 'hidden' class
    const form = editForm.querySelector(".menu-item-form");

    // Toggle the 'hidden' class to show or hide the form
    form.classList.toggle("hidden");
  });
});
