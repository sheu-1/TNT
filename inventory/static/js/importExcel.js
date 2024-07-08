document
  .getElementById("import-excel-btn")
  .addEventListener("click", function () {
    document.getElementById("file-input").click();
  });

document
  .getElementById("file-input")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    console.log(formData);

    fetch("/upload_excel", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Data imported successfully!");
        } else {
          alert("Error: " + data.message);
        }
      })
      .catch((error) => {
        console.error("Fetch error:", error);
        alert("An error occurred while uploading the file.");
      });
  });
