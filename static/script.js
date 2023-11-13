
document.addEventListener("DOMContentLoaded", function() {
    // Get reference to the dropdown filter and table rows
    const statusFilter = document.getElementById('statusFilter');
    const tableRows = document.querySelectorAll("#taskTable tbody tr");

    if (statusFilter) {
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
    } else {
        console.error("Element with ID 'statusFilter' not found!");
    }
});

// function searchProjects() {
//     let input = document.getElementById('projectSearch').value.toLowerCase();
//     let projectCards = document.getElementsByClassName('card');

//     for (let i = 0; i < projectCards.length; i++) {
//       let title = projectCards[i].querySelector('.card-title').textContent.toLowerCase();
//       if (title.includes(input)) {
//         projectCards[i].style.display = "";
//       } else {
//         projectCards[i].style.display = "none";
//       }
//     }
//   }



  function searchProjects() {
    let input = document.getElementById('projectSearch').value.toLowerCase();

    // Sending an AJAX request to the Flask server
    fetch('/search?query=' + input)
        .then(response => response.json())
        .then(data => {
            // Assuming 'data' is the list of projects returned from the server
            updateProjectCards(data.projects);
        });
}

function updateProjectCards(projects) {
    // Clear existing project cards
    let projectsContainer = document.getElementById('projects-container');
    projectsContainer.innerHTML = '';

    // Add new project cards based on the data received
    projects.forEach(project => {
        let cardHtml = `<div class="card">
                            <div class="card-title">${project.name}</div>
                            <a href="/project/${project.project_id}" class="card-title">${project.name}</a>
                            <div class="card-body">${project.description}</div>
                        </div>`;
        projectsContainer.innerHTML += cardHtml;
    });
}