// =========================
// PWA SERVICE WORKER
// =========================

if ("serviceWorker" in navigator) {

    window.addEventListener(
        "load",
        () => {

            navigator.serviceWorker
                .register("/static/js/service-worker.js")
                .then((registration) => {

                    console.log(
                        "Service Worker registered:",
                        registration
                    );

                })
                .catch((error) => {

                    console.error(
                        "Service Worker registration failed:",
                        error
                    );

                });

        }
    );

}


// =========================
// INSTALL PROMPT
// =========================
let deferredPrompt;

window.addEventListener(
    "beforeinstallprompt",
    (event) => {

        event.preventDefault();

        deferredPrompt = event;

        console.log(
            "PWA install prompt available"
        );

    }
);


// =========================
// INSTALL APP
// =========================
async function installPWA() {

    if (!deferredPrompt) return;

    deferredPrompt.prompt();

    const { outcome } =
        await deferredPrompt.userChoice;

    console.log(
        `User response: ${outcome}`
    );

    deferredPrompt = null;

}