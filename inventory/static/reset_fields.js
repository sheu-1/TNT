const resetBtn = document.querySelector("#reset-btn");

resetBtn.addEventListener("click", (e) => {
  e.preventDefault();
  window.location.href = "/assets/create";
});
