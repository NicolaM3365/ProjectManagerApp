

document.addEventListener("DOMContentLoaded", function() {
    // Get reference to the dropdown filter and table rows
    const statusFilter = document.getElementById('statusFilter');
    const tableRows = document.querySelectorAll("#taskTable tbody tr");

    // Attach event listener to the dropdown filter
    statusFilter.addEventListener("change", function() {
        const selectedStatus = statusFilter.value;

        tableRows.forEach(function(row) {
            const statusCell = row.querySelector(".task-status");
            if (!selectedStatus || statusCell.innerText === selectedStatus) {
                row.style.display = ""; // show the row
            } else {
                row.style.display = "none"; // hide the row
            }
        });
    });
});



