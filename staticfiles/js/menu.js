// Toggle the "Add New" menu item form
const addMenuItemButtons = document.querySelectorAll(".add-btn");

addMenuItemButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault();
    const category = button.getAttribute("data-category");
    const form = document.querySelector(
      `.category-form[data-category="${category}"] .menu-item-form`
    );
    form.classList.toggle("hidden");
  });
});

// Edit menu item functionality
const editButtons = document.querySelectorAll(".edit-btn");

editButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    e.preventDefault();
    const menuItemId = e.target.getAttribute("data-menu-item-id");

    // Retrieve and populate the form fields with current menu item values
    const menuItemName = document.getElementById(
      `menu-item-name-${menuItemId}`
    ).innerText;
    const menuItemDescription = document.getElementById(
      `menu-item-description-${menuItemId}`
    ).innerText;
    const menuItemPrice = document.getElementById(
      `menu-item-price-${menuItemId}`
    ).innerText;
    const menuItemIsAvailable = document.getElementById(
      `menu-item-is-available-${menuItemId}`
    ).innerText;

    const editForm = document.getElementById(`edit-form-${menuItemId}`);
    const formFields = {
      name: editForm.querySelector("input[name='name']"),
      description: editForm.querySelector("textarea[name='description']"),
      price: editForm.querySelector("input[name='price']"),
      isAvailable: editForm.querySelector("input[name='is_available']"),
    };

    // Populate the form fields
    formFields.name.value = menuItemName;
    formFields.description.value = menuItemDescription;
    formFields.price.value = menuItemPrice;
    formFields.isAvailable.value = menuItemIsAvailable;

    // Toggle the form visibility
    editForm.querySelector(".menu-item-form").classList.toggle("hidden");
  });
});

// Image preview functionality
function handleImagePreview(input) {
  const file = input.files[0];
  const previewImage = document.getElementById("image-preview");

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImage.src = e.target.result;
      previewImage.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
  } else {
    previewImage.classList.add("hidden");
  }
}

// Event listener for image input
const imageInput = document.querySelector("input[name='image']");
if (imageInput) {
  imageInput.addEventListener("change", () => handleImagePreview(imageInput));
}

// Delete menu item functionality with confirmation modal
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.querySelectorAll(".delete-btn");
const deleteConfirm = document.getElementById("delete-confirm");

deleteButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    const menuItemId = e.target.getAttribute("data-menu-item-id");
    deleteConfirm.href = `/menu/delete-menu-item/${menuItemId}`;
    deleteModal.show();
  });
});

// Update and show modal with menu item details
const menuItemTitles = document.querySelectorAll(".menu-item-title");

menuItemTitles.forEach((title) => {
  title.addEventListener("click", (e) => {
    const menuItemId = e.target.getAttribute("data-bs-target").split("-")[1];
    const modal = document.getElementById(`menuItemModal-${menuItemId}`);
    const menuItemName = document.getElementById(
      `menu-item-name-${menuItemId}`
    ).innerText;
    const menuItemDescription = document.getElementById(
      `menu-item-description-${menuItemId}`
    ).innerText;
    const menuItemPrice = document.getElementById(
      `menu-item-price-${menuItemId}`
    ).innerText;
    const menuItemIsAvailable = document.getElementById(
      `menu-item-is-available-${menuItemId}`
    ).innerText;

    // Update modal content
    modal.querySelector(".modal-title").innerText = menuItemName;
    modal.querySelector(".modal-body").innerHTML = `
      <img src="${
        document.getElementById(`menu-item-image-${menuItemId}`).src
      }" alt="${menuItemName}" class="img-fluid">
      <h5>Description:</h5>
      <p>${menuItemDescription}</p>
      <h5>Price:</h5>
      <p>£${menuItemPrice}</p>
      <h5>Available:</h5>
      <p>${menuItemIsAvailable === "True" ? "Yes" : "No"}</p>
    `;
  });
});

// // Select all the forms with the class 'menu-item-form'
// const forms = document.querySelectorAll(".menu-item-form");

// // Loop through each form
// forms.forEach((form) => {
//   // Extract the ID number from the form's action URL
//   const formAction = form.action;
//   const idNumber = formAction.split("/").filter(Boolean).pop(); // Get the number from the URL

//   // Target all the divs inside the form and modify their ids and children's ids
//   const divs = form.querySelectorAll('div[id^="div_id_"]');

//   divs.forEach((div) => {
//     const originalId = div.id;
//     const label = div.querySelector("label");
//     const input = div.querySelector("input, textarea"); // This works for both input and textarea

//     // Append the ID number to the div, label, and input elements' ids
//     div.id = `${originalId}-${idNumber}`;

//     if (label) {
//       label.setAttribute("for", `${label.getAttribute("for")}-${idNumber}`);
//     }

//     if (input) {
//       input.id = `${input.id}-${idNumber}`;
//     }
//   });
// });
