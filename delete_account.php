<?php
session_start();

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "new";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch user data from session
$user_id = $_SESSION['user_id'];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Delete the user from the database
    $stmt = $conn->prepare("DELETE FROM users WHERE id = ?");
    $stmt->bind_param("i", $user_id);

    if ($stmt->execute()) {
        echo "Account deleted successfully.";
        // Destroy session and redirect to homepage or login page
        session_destroy();
        header("Location: index.html");
        exit();
    } else {
        echo "Error deleting account: " . $stmt->error;
    }

    $stmt->close();
}

$conn->close();
?>
