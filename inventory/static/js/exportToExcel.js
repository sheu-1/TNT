function getRandomNumbers() {
  let dateObj = new Date();
  let dateTime = `${dateObj.getHours()}${dateObj.getMinutes()}${dateObj.getSeconds()}`;

  return `${dateTime}${Math.floor(Math.random().toFixed(2) * 100)}`;
}
const search = document.querySelector(".input-group input"),
  table_rows = document.querySelectorAll("tbody tr"),
  table_headings = document.querySelectorAll("thead th");

// 1. Searching for specific data of HTML table
search.addEventListener("input", searchTable);

function searchTable() {
  table_rows.forEach((row, i) => {
    let table_data = row.textContent.toLowerCase(),
      search_data = search.value.toLowerCase();

    row.classList.toggle("hide", table_data.indexOf(search_data) < 0);
    row.style.setProperty("--delay", i / 25 + "s");
  });

  document.querySelectorAll("tbody tr:not(.hide)").forEach((visible_row, i) => {
    visible_row.style.backgroundColor =
      i % 2 == 0 ? "transparent" : "#0000000b";
  });
}

// 2. Sorting | Ordering data of HTML table

table_headings.forEach((head, i) => {
  let sort_asc = true;
  head.onclick = () => {
    table_headings.forEach((head) => head.classList.remove("active"));
    head.classList.add("active");

    document
      .querySelectorAll("td")
      .forEach((td) => td.classList.remove("active"));
    table_rows.forEach((row) => {
      row.querySelectorAll("td")[i].classList.add("active");
    });

    head.classList.toggle("asc", sort_asc);
    sort_asc = head.classList.contains("asc") ? false : true;

    sortTable(i, sort_asc);
  };
});

function sortTable(column, sort_asc) {
  [...table_rows]
    .sort((a, b) => {
      let first_row = a
          .querySelectorAll("td")
          [column].textContent.toLowerCase(),
        second_row = b.querySelectorAll("td")[column].textContent.toLowerCase();

      return sort_asc
        ? first_row < second_row
          ? 1
          : -1
        : first_row < second_row
          ? -1
          : 1;
    })
    .map((sorted_row) =>
      document.querySelector("tbody").appendChild(sorted_row),
    );
}
// 6. Converting HTML table to EXCEL File

const excel_btn = document.querySelector("#toEXCEL");

const toExcel = function (table) {
  const t_heads = table.querySelectorAll("th"),
    tbody_rows = table.querySelectorAll("tbody tr");

  const headings = [...t_heads].map((head) => {
    let actual_head = head.textContent.trim().split(" ");
    return actual_head.splice(0, actual_head.length - 1).join(" ");
  });

  const table_data = [...tbody_rows].map((row) => {
    const cells = row.querySelectorAll("td");
    const data_without_img = [...cells].map((cell) => cell.textContent.trim());
    return data_without_img;
  });

  // Combine headings and table data into an array of arrays
  const data = [headings, ...table_data];

  // Create a workbook and add a worksheet with the data
  const ws = XLSX.utils.aoa_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

  // Generate binary string and return
  return XLSX.write(wb, { bookType: "xlsx", type: "binary" });
};

function s2ab(s) {
  const buf = new ArrayBuffer(s.length);
  const view = new Uint8Array(buf);
  for (let i = 0; i !== s.length; ++i) view[i] = s.charCodeAt(i) & 0xff;
  return buf;
}

excel_btn.onclick = () => {
  const excel = toExcel(customers_table);
  const blob = new Blob([s2ab(excel)], {
    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  });
  saveAs(blob, "inventory.xlsx");
};
