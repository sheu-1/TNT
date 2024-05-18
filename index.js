const reset = document.querySelector("#reset");
const formInput = document.querySelectorAll("input");

reset.addEventListener("click", (e) => {
  e.preventDefault();
  formInput.forEach((input) => (input.value = ""));
});
