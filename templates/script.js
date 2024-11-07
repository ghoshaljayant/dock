// Function to update the clock every second
function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('clock').innerText = hours + ':' + minutes + ':' + seconds;
}
setInterval(updateClock, 1000); // Update every second

function sendRequest(buttonValue) {
    fetch('/run-function', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ function: buttonValue })
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}

// Initialize the clock when the page loads
window.onload = updateClock;
