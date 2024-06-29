document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".editable").forEach(function (td) {
    td.addEventListener("dblclick", function () {
      var input = document.createElement("input");
      input.type = "text";
      input.value = td.innerHTML;
      input.classList.add("edit-input");

      input.addEventListener("blur", function () {
        var field = td.getAttribute("data-field");
        var id = td.getAttribute("data-id");
        var value = input.value;

        fetch("/update_asset", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            id: id,
            field: field,
            value: value,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              td.innerHTML = value;
            } else {
              alert("Failed to update asset");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });

        td.removeChild(input);
        td.innerHTML = value;
      });

      td.innerHTML = "";
      td.appendChild(input);
      input.focus();
    });
  });
});
