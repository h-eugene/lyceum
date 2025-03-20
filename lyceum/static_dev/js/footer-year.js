document.addEventListener("DOMContentLoaded", function() {
    const serverTimestamp = parseInt(document.getElementById("year").dataset.serverTime);
    const serverTime = new Date(serverTimestamp * 1000);
    const serverYear = serverTime.getFullYear();

    const clientDate = new Date();
    const clientYear = clientDate.getFullYear();

    const timeDiff = Math.abs(clientDate - serverTime);
    const oneDay = 24 * 60 * 60 * 1000;

    const displayYear = (timeDiff > oneDay) ? serverYear : clientYear;

    document.getElementById("year").textContent = displayYear;
});
