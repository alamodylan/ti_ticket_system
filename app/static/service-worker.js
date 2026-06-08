// =========================
// CACHE NAME
// =========================
const CACHE_NAME = "tickets-ti-v1";


// =========================
// FILES TO CACHE
// =========================
const urlsToCache = [

    "/",

    "/static/css/main.css",
    "/static/css/dashboard.css",
    "/static/css/variables.css",

    "/static/js/app.js",
    "/static/js/dashboard.js",
    "/static/js/tickets.js",
    "/static/js/notifications.js",
    "/static/js/pwa.js",

];


// =========================
// INSTALL EVENT
// =========================
self.addEventListener(
    "install",
    (event) => {

        console.log(
            "Service Worker installing..."
        );

        event.waitUntil(

            caches.open(CACHE_NAME)
                .then((cache) => {

                    return cache.addAll(
                        urlsToCache
                    );

                })

        );

        self.skipWaiting();

    }
);


// =========================
// ACTIVATE EVENT
// =========================
self.addEventListener(
    "activate",
    (event) => {

        console.log(
            "Service Worker activated"
        );

        event.waitUntil(

            caches.keys()
                .then((cacheNames) => {

                    return Promise.all(

                        cacheNames.map((cache) => {

                            if (
                                cache !== CACHE_NAME
                            ) {

                                return caches.delete(
                                    cache
                                );

                            }

                        })

                    );

                })

        );

        self.clients.claim();

    }
);


// =========================
// FETCH EVENT
// =========================
self.addEventListener(
    "fetch",
    (event) => {

        event.respondWith(

            caches.match(event.request)
                .then((response) => {

                    // RETURN CACHE
                    if (response) {

                        return response;

                    }

                    // FETCH NETWORK
                    return fetch(
                        event.request
                    );

                })

        );

    }
);


// =========================
// PUSH NOTIFICATIONS
// =========================
self.addEventListener(
    "push",
    (event) => {

        const data = event.data
            ? event.data.json()
            : {};

        const title =
            data.title ||
            "Sistema de Tickets";

        const options = {

            body:
                data.body ||
                "Nueva notificación",

            icon:
                "/static/icons/icon-192x192.png",

            badge:
                "/static/icons/icon-72x72.png",

            vibrate: [200, 100, 200],

            data: {

                url:
                    data.url || "/"

            }

        };

        event.waitUntil(

            self.registration.showNotification(
                title,
                options
            )

        );

    }
);


// =========================
// NOTIFICATION CLICK
// =========================
self.addEventListener(
    "notificationclick",
    (event) => {

        event.notification.close();

        event.waitUntil(

            clients.openWindow(
                event.notification.data.url
            )

        );

    }
);