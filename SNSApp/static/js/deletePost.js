const modal = document.getElementById("deleteModal");
const cancelBtn = document.getElementById("cancelDelete");
const confirmBtn = document.getElementById("confirmDelete");

let currentForm = null;

document.querySelectorAll(".delete-btn").forEach(button => {
  button.addEventListener("click", function () {
    currentForm = this.closest("form");
    modal.classList.add("active");
  });
});

cancelBtn.addEventListener("click", function () {
  modal.classList.remove("active");
});

confirmBtn.addEventListener("click", function () {
  if (currentForm) {
    currentForm.submit();
  }
});
