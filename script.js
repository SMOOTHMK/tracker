const statusText = document.getElementById("status");

function getLocation() {
    if (!navigator.geolocation) {
        statusText.textContent = "Location is not supported by this browser.";
        return;
    }

    statusText.textContent = "Requesting location permission...";

    navigator.geolocation.getCurrentPosition(
        async function(position) {
            const locationData = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy: position.coords.accuracy,
                browser: navigator.userAgent
            };

            statusText.textContent = "Submitting your approved location...";

            try {
                const response = await fetch("/collect", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(locationData)
                });

                const result = await response.json();

                if (!response.ok || !result.success) {
                    throw new Error(result.message || "Location submission failed.");
                }

                statusText.textContent = "Successful. Redirecting...";
                window.location.replace("https://example.com");

            } catch (error) {
                statusText.textContent = error.message;
            }
        },

        function(error) {
            if (error.code === 1) {
                statusText.textContent = "Location permission denied.";
            } else if (error.code === 2) {
                statusText.textContent = "Location is unavailable.";
            } else {
                statusText.textContent = "Location request timed out.";
            }
        },

        {
            enableHighAccuracy: true,
            timeout: 20000,
            maximumAge: 0
        }
    );
}

getLocation();
