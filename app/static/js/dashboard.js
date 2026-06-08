// =========================
// DASHBOARD JS
// =========================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeStatsAnimation();

    }
);


// =========================
// STATS ANIMATION
// =========================
function initializeStatsAnimation() {

    const stats = document.querySelectorAll(
        ".card h2"
    );

    stats.forEach((stat) => {

        const finalValue = parseInt(
            stat.innerText
        );

        if (isNaN(finalValue)) return;

        let currentValue = 0;

        const increment = Math.ceil(
            finalValue / 40
        );

        const counter = setInterval(() => {

            currentValue += increment;

            if (currentValue >= finalValue) {

                stat.innerText = finalValue;

                clearInterval(counter);

            } else {

                stat.innerText = currentValue;

            }

        }, 30);

    });

}