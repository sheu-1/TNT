<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $email = $_POST["email"];
    $password = $_POST["password"];

    // Database connection
    $servername = 'localhost';
    $username = 'root';
    $passwordDB = ''; // Assuming no password for root user
    $dbname = 'new';

    $conn = mysqli_connect($servername, $username, $passwordDB, $dbname);

    // Check connection
    if (mysqli_connect_error()) {
        exit('Error connecting to the database: ' . mysqli_connect_error());
    }

    // Prepare and execute query to fetch user data
    $stmt = $conn->prepare("SELECT id, password FROM login WHERE email = ?");
    $stmt->bind_param('s', $email);
    $stmt->execute();
    $stmt->store_result();

    // Check if the user exists
    if ($stmt->num_rows > 0) {
        $stmt->bind_result($userId, $hashedPassword);
        $stmt->fetch();

        // Verify the password
        if (password_verify($password, $hashedPassword)) {
            $_SESSION["user_id"] = $userId; // Store user ID in the session
            header("Location: dashboard.html"); // Redirect to the dashboard
            exit();
        } else {
            $error = "Invalid credentials. Please try again.";
        }
    } else {
        $error = "Invalid credentials. Please try again.";
    }

    $stmt->close();
    $conn->close();
}

if (isset($error)) {
    echo $error;
}
?>
