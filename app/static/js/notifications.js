// =========================
// NOTIFICATIONS JS
// =========================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeNotifications();

    }
);


// =========================
// INITIALIZE
// =========================
function initializeNotifications() {

    const notificationButton =
        document.querySelector(
            "#notificationButton"
        );

    if (!notificationButton) return;

    notificationButton.addEventListener(
        "click",
        fetchNotifications
    );

}


// =========================
// FETCH NOTIFICATIONS
// =========================
async function fetchNotifications() {

    try {

        const response = await fetch(
            "/notifications/api/unread"
        );

        const data = await response.json();

        console.log(
            "Notifications:",
            data
        );

    } catch (error) {

        console.error(
            "Error loading notifications:",
            error
        );

    }

}


// =========================
// MARK AS READ
// =========================
async function markNotificationAsRead(
    notificationId
) {

    try {

        await fetch(
            `/notifications/read/${notificationId}`,
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(
            "Error marking notification:",
            error
        );

    }

}