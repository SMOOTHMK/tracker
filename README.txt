TRACKER BY SMOOTH

Requirements:
- PHP installed and available from Command Prompt.
- A browser with location permission support.
- For public hosting, use HTTPS.

Run locally:
1. Extract this ZIP.
2. Open Command Prompt in the Tracker-by-Smooth folder.
3. Run: php -S localhost:8080
4. Open: http://localhost:8080

When the page opens, it explains that location information will be submitted.
The browser then asks for location permission. If the visitor allows it,
the browser-provided coordinates and accuracy are submitted to collect.php.
The server appends a record to location.txt and prints it in the PHP terminal.

Before using:
- Open script.js and replace https://example.com with your intended destination.
- Keep the disclosure on the page.
- Do not publish location records or expose location.txt publicly.
- Browser geolocation reports the device's estimated accuracy; the code cannot
  guarantee a particular GPS precision.
- localhost is treated as a secure context for local testing. Public websites
  need HTTPS for browser geolocation.
