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
