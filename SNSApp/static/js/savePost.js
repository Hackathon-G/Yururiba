document.querySelectorAll(".save-btn").forEach(button => {
  button.addEventListener("click", function () {
    const icon = this.querySelector(".icon");

    this.classList.toggle("saved");

    if (this.classList.contains("saved")) {
      icon.textContent = "bookmark";
    } else {
      icon.textContent = "bookmark_border";
    }
  });
});
