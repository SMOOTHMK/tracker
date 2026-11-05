const shareButton = document.getElementById("shareButton");
const statusText = document.getElementById("status");

shareButton.addEventListener("click", gpsLocation);

function gpsLocation() {
    if (!navigator.geolocation) {
        statusText.textContent = "Location services are not supported by this browser.";
        return;
    }

    shareButton.disabled = true;
    statusText.textContent = "Waiting for your browser's location permission...";

    navigator.geolocation.getCurrentPosition(
        async function (position) {
            const locationData = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy: position.coords.accuracy,
                browser: navigator.userAgent
            };

            statusText.textContent = "Sending the information you approved...";

            try {
                const response = await fetch("collect.php", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(locationData)
                });

                const result = await response.json();

                if (!response.ok || !result.success) {
                    throw new Error(result.message || "The server could not save the information.");
                }

                statusText.textContent = "Location submitted successfully. Redirecting...";
                window.location.replace("https://example.com");
            } catch (error) {
                statusText.textContent = "Could not submit location: " + error.message;
                shareButton.disabled = false;
            }
        },
        function (error) {
            const messages = {
                1: "Location permission was denied.",
                2: "Your location is currently unavailable.",
                3: "The location request timed out."
            };

            statusText.textContent = messages[error.code] || "Unable to get your location.";
            shareButton.disabled = false;
        },
        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }
    );
}
