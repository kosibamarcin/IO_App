/**
 *
 * @param {HTMLTableElement} table The table to sort
 * @param {number} column The index of the column to sort
 * @param {boolean} asc Determines if the sorting will be in ascending order
 */

function sortTable(table, column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"))

    // Sort each row
    const sortedRows = rows.sort((a, b) => {
        const aColText = a.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();

        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    });

    // Remove all existing table rows from the table
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    // Re-add rows but sorted
    tBody.append(...sortedRows);

    // Remember the current order (as "th-sort-asc" or "th-sort-desc" th class)
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${ column + 1 })`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${ column + 1 })`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".table-sortable th").forEach(headerCell => {
   headerCell.addEventListener("click", () => {
      const tableElement = headerCell.parentElement.parentElement.parentElement;
      const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
      const currentIsAscending = headerCell.classList.contains("th-sort-asc");

      sortTable(tableElement, headerIndex, !currentIsAscending);
   });
});

function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res)=>{
        window.location.href = '/activity';
    });
}
