GPSFinder - Educational GPS Location Sharing Demonstration

PROJECT CONTENTS
- index.html: explains the demonstration and asks the visitor to choose to share.
- script.js: requests browser location permission after the visitor clicks the button,
  then sends the approved coordinates to the PHP receiver.
- collect.php: validates the submitted values, saves them in location.txt,
  and prints the received record to the PHP development server terminal.
- location.txt: created automatically after the first successful submission.

HOW TO RUN ON WINDOWS
1. Install PHP and make sure the php command works in Command Prompt.
2. Open Command Prompt in this GPSFinder folder.
3. Run: php -S localhost:8000
4. Open: http://localhost:8000
5. Read the notice and click "Agree and Share Location".
6. Grant location permission in the browser.
7. Check the running terminal and location.txt for the submitted record.

IMPORTANT
- Browser geolocation requires HTTPS on deployed websites. localhost is allowed for testing.
- The visitor must explicitly click the button and grant browser location permission.
- The IP address is the address seen by the PHP server; behind a proxy it may be the proxy address.
- The browser user-agent is a browser-provided description and may not uniquely identify a device.
- Replace https://example.com in script.js with your intended destination URL.
- Keep location.txt private. Do not publish it or expose it through a public download link.
- This is a local educational demonstration. Do not collect or share anyone's location without
  clear notice and their informed permission.
