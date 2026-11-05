<?php
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["success" => false, "message" => "POST requests only."]);
    exit;
}

$data = json_decode(file_get_contents("php://input"), true);

if (
    !is_array($data) ||
    !isset($data["latitude"], $data["longitude"], $data["accuracy"], $data["browser"])
) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "Required information is missing."]);
    exit;
}

$latitude = filter_var($data["latitude"], FILTER_VALIDATE_FLOAT);
$longitude = filter_var($data["longitude"], FILTER_VALIDATE_FLOAT);
$accuracy = filter_var($data["accuracy"], FILTER_VALIDATE_FLOAT);

if (
    $latitude === false ||
    $longitude === false ||
    $accuracy === false ||
    $latitude < -90 || $latitude > 90 ||
    $longitude < -180 || $longitude > 180 ||
    $accuracy < 0
) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "Invalid coordinate values."]);
    exit;
}

$ip = $_SERVER["REMOTE_ADDR"] ?? "Unavailable";
$browser = substr((string)$data["browser"], 0, 1000);
$time = date("Y-m-d H:i:s");

$entry = "GPSFinder Record\n";
$entry .= "Time: " . $time . "\n";
$entry .= "IP: " . $ip . "\n";
$entry .= "Latitude: " . $latitude . "\n";
$entry .= "Longitude: " . $longitude . "\n";
$entry .= "Accuracy: " . $accuracy . " meters\n";
$entry .= "Browser: " . $browser . "\n";
$entry .= "------------------------------\n";

$file = __DIR__ . DIRECTORY_SEPARATOR . "location.txt";

if (file_put_contents($file, $entry, FILE_APPEND | LOCK_EX) === false) {
    http_response_code(500);
    echo json_encode(["success" => false, "message" => "Could not write location.txt."]);
    exit;
}

/* PHP's built-in development server displays this in its running terminal. */
error_log(trim($entry));

echo json_encode(["success" => true]);
?>
