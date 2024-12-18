// Get Buttons
const addMenuItemButton = document.getElementById("addMenuItemButton");

// Get Form
const menuItemForm = document.getElementById("menuItemForm");

// Add click event listener to the "Add Menu Item" button
addMenuItemButton.addEventListener("click", (e) => {
  e.preventDefault();
  // Toggle the 'hidden' class to show or hide the form
  menuItemForm.classList.toggle("hidden");
});
