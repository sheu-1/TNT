<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "new";

$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (mysqli_connect_errno()) {
    exit("Error connecting: " . mysqli_connect_error());
}

// Check if form data is set
if (!isset($_POST['description'], $_POST['room'], $_POST['serial'], $_POST['building'], $_POST['productnumber'], $_POST['makemodel'], $_POST['state'])) {
    exit("Please fill all fields");
}

// Validate input
$description = $_POST['description'];
$room = $_POST['room'];
$serial = $_POST['serial'];
$building = $_POST['building'];
$productnumber = $_POST['productnumber'];
$makemodel = $_POST['makemodel'];
$state = $_POST['state'];

if (empty($description) || empty($room) || empty($serial) || empty($building) || empty($productnumber) || empty($makemodel) || empty($state)) {
    exit('Fields cannot be empty');
}

// Check if the asset already exists
$stmt = $conn->prepare("SELECT serial FROM assets WHERE serial = ?");
$stmt->bind_param('s', $serial);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    echo "Asset already exists";
} else {
    // Prepare statement to insert new asset
    $stmt = $conn->prepare("INSERT INTO assets (description, room, serial, building, productnumber, makemodel, state) VALUES (?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("sssssss", $description, $room, $serial, $building, $productnumber, $makemodel, $state);

    if ($stmt->execute()) {
        echo "Successfully registered.";
    } else {
        echo "Error occurred while registering.";
    }
}

$stmt->close();
$conn->close();
?>
