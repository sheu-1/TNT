document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("tr[data-href]").forEach(function (row) {
    row.addEventListener("dblclick", function () {
      window.location = this.dataset.href;
    });
  });
});
