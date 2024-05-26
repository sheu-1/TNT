const copyrightYear = document.querySelector(".copyright-year");
console.log(copyrightYear);
copyrightYear.textContent = new Date().getFullYear();

const filterBtn = document.querySelector("#tbl");

document.addEventListener("DOMContentLoaded", () => (filterBtn.value = ""));
