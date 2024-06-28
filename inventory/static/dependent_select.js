document.addEventListener("DOMContentLoaded", function () {
  var directorateSelect = document.getElementById("directorate");
  var unitsSelect = document.getElementById("units");

  directorateSelect.addEventListener("change", function () {
    var directorate = directorateSelect.value;
    fetch("/get_units", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ directorate: directorate }),
    })
      .then((response) => response.json())
      .then((data) => {
        unitsSelect.innerHTML = "";
        data.forEach(function (unit) {
          var option = document.createElement("option");
          option.value = unit;
          option.textContent = unit;
          unitsSelect.appendChild(option);
        });
      });
  });

  // Trigger change event on page load to populate the items select field with default category
  var event = new Event("change");
  directorateSelect.dispatchEvent(event);
});
