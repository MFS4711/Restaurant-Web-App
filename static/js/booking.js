// JS for bootstrap Modal:
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
// Delete buttons
const deleteButtons = document.getElementsByClassName("delete-btn");
const deleteConfirm = document.getElementById("delete-confirm");

/**
 * Initializes deletion functionality for the provided delete buttons.
 *
 * For each button in the `deleteButtons` collection:
 * - Retrieves the associated booking ID upon click.
 * - Updates the `deleteConfirm` link's href to point to the deletion endpoint for the specific booking.
 * - Displays a confirmation modal (`deleteModal`) to prompt the user for confirmation before deletion.
 */
for (let button of deleteButtons) {
  button.addEventListener("click", (e) => {
    let bookingId = e.target.getAttribute("data-booking-id");
    deleteConfirm.href = `/delete-booking/${bookingId}/`;
    deleteModal.show();
  });
}