const copyrightYear = document.querySelector(".copyright-year");
const filterBtn = document.querySelector("#tbl");
const sortBtn = document.querySelector("#sort-btn");
console.log(copyrightYear);
copyrightYear.textContent = new Date().getFullYear();

document.addEventListener("DOMContentLoaded", () => {
  filterBtn.value = "";
  sortBtn.value = "sort";
});
