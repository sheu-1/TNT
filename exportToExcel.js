const exportExcelBtn = document.querySelector("#export-excel-btn");
exportExcelBtn.addEventListener("click", exportToExcel);
function exportToExcel(tableId) {
  tableId = "table";
  let tableData = document.getElementById(tableId).outerHTML;
  tableData = tableData.replace(/<A[^>]*>|<\/A>/g, ""); //remove if u want links in your table
  tableData = tableData.replace(/<input[^>]*>|<\/input>/gi, ""); //remove input params

  let a = document.createElement("a");
  a.href = `data:application/vnd.ms-excel, ${encodeURIComponent(tableData)}`;
  a.download = "downloaded_file_" + getRandomNumbers() + ".xls";
  a.click();
}
function getRandomNumbers() {
  let dateObj = new Date();
  let dateTime = `${dateObj.getHours()}${dateObj.getMinutes()}${dateObj.getSeconds()}`;

  return `${dateTime}${Math.floor(Math.random().toFixed(2) * 100)}`;
}
