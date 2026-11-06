const statusText = document.getElementById("status");
const shareButton = document.getElementById("shareButton");
const mapLink = document.getElementById("mapLink");

shareButton.addEventListener("click", function () {
    if (!navigator.geolocation) {
        statusText.textContent = "Location is not supported by this browser.";
        return;
    }

    if (!window.isSecureContext) {
        statusText.textContent =
            "HTTPS is required for location access on this device.";
        return;
    }

    shareButton.disabled = true;
    statusText.textContent = "Requesting location permission...";

    navigator.geolocation.getCurrentPosition(
        async function (position) {
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
                    throw new Error(result.message || "Submission failed.");
                }

                statusText.textContent = result.message;

                mapLink.href = result.map;
                mapLink.hidden = false;

            } catch (error) {
                statusText.textContent = error.message;
            } finally {
                shareButton.disabled = false;
            }
        },

        function (error) {
            if (error.code === 1) {
                statusText.textContent = "Location permission denied.";
            } else if (error.code === 2) {
                statusText.textContent = "Location is unavailable.";
            } else {
                statusText.textContent = "Location request timed out.";
            }

            shareButton.disabled = false;
        },

        {
            enableHighAccuracy: true,
            timeout: 20000,
            maximumAge: 0
        }
    );
});
