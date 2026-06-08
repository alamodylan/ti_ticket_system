// =========================
// TICKETS JS
// =========================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeTicketSearch();
        initializePriorityColors();

    }
);


// =========================
// SEARCH FILTER
// =========================
function initializeTicketSearch() {

    const searchInput = document.querySelector(
        'input[placeholder="Buscar ticket..."]'
    );

    if (!searchInput) return;

    searchInput.addEventListener(
        "keyup",
        function () {

            const filter = this.value.toLowerCase();

            const rows = document.querySelectorAll(
                "table tbody tr"
            );

            rows.forEach((row) => {

                const text = row.innerText.toLowerCase();

                row.style.display = text.includes(filter)
                    ? ""
                    : "none";

            });

        }
    );

}


// =========================
// PRIORITY COLORS
// =========================
function initializePriorityColors() {

    const badges = document.querySelectorAll(
        ".badge"
    );

    badges.forEach((badge) => {

        const text = badge.innerText.trim();

        if (text === "Crítica") {

            badge.classList.add("bg-danger");

        }

        else if (text === "Alta") {

            badge.classList.add("bg-warning");

        }

        else if (text === "Media") {

            badge.classList.add("bg-primary");

        }

        else if (text === "Baja") {

            badge.classList.add("bg-success");

        }

    });

}