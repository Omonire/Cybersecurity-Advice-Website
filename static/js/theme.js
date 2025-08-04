function toggleTheme() {
    document.body.classList.toggle("light-mode");
    localStorage.setItem("theme", document.body.classList.contains("light-mode") ? "light" : "dark");
}
window.onload = function() {
    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light-mode");
    }
}
function showLoader() {
    let loader = document.getElementById("loading-screen");
    let text = document.getElementById("loading-text");
    loader.classList.remove("hidden");

    let percent = 0;
    let interval = setInterval(() => {
        percent += Math.floor(Math.random() * 10) + 5; // Increase randomly
        if (percent >= 100) {
            percent = 100;
            clearInterval(interval);
            loader.classList.add("hidden");
        }
        text.textContent = percent + "%";
    }, 100);
}

document.addEventListener("DOMContentLoaded", () => {
    // Show loader when any link is clicked
    document.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", (e) => {
            if (link.getAttribute("href").startsWith("#") || link.getAttribute("target") === "_blank") return;
            showLoader();
        });
    });

    // Show loader on page refresh
    showLoader();
});
