document.addEventListener("DOMContentLoaded", () => {
  const deleteButtons = document.querySelectorAll(".delete-btn");

  deleteButtons.forEach((button) => {
    const assetId = button.getAttribute("data-id");
    const modalForm = document.querySelector(
      `.delete-modal[data-id='${assetId}']`,
    );
    const cancelBtn = modalForm.querySelector(".cancel-btn");

    button.addEventListener("click", () => {
      modalForm.showModal();
    });

    cancelBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modalForm.close();
    });
  });
});
