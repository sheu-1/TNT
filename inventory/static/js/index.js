const copyrightYear = document.querySelector(".copyright-year");
const filterBtn = document.querySelector("#tbl");
const errorMessageContainer = document.querySelector(
  "#error-message-container",
);
const closeErrorBtn = document.querySelector("#close-error-btn");
console.log(copyrightYear);
copyrightYear.textContent = new Date().getFullYear();

document.addEventListener("DOMContentLoaded", () => (filterBtn.value = ""));
document.addEventListener("DOMContentLoaded", () => {
  filterBtn.value = "";
  sortBtn.value = "sort";
});

closeErrorBtn.addEventListener("click", () => {
  errorMessageContainer.setAttribute("style", "display:none;");
});

setTimeout(() => {
  errorMessageContainer.setAttribute("style", "display:none;");
}, 3000);
