// =========================
// GLOBAL APP JS
// =========================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeTooltips();
        initializeAlerts();
        initializeDropdowns();

    }
);


// =========================
// TOOLTIPS
// =========================
function initializeTooltips() {

    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        )
    );

    tooltipTriggerList.map((tooltipTriggerEl) => {

        return new bootstrap.Tooltip(
            tooltipTriggerEl
        );

    });

}


// =========================
// ALERT AUTO CLOSE
// =========================
function initializeAlerts() {

    const alerts = document.querySelectorAll(
        ".alert"
    );

    alerts.forEach((alert) => {

        setTimeout(() => {

            const bsAlert = bootstrap.Alert.getOrCreateInstance(
                alert
            );

            bsAlert.close();

        }, 5000);

    });

}


// =========================
// DROPDOWNS
// =========================
function initializeDropdowns() {

    const dropdownElementList = [].slice.call(
        document.querySelectorAll(
            ".dropdown-toggle"
        )
    );

    dropdownElementList.map((dropdownToggleEl) => {

        return new bootstrap.Dropdown(
            dropdownToggleEl
        );

    });

}


// =========================
// CONFIRM DELETE
// =========================
function confirmDelete(message = "¿Desea eliminar este registro?") {

    return confirm(message);

}