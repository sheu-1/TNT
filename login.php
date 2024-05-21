<?php
$servername = 'localhost';
$username = 'root';
$password = '';
$dbname = 'new';

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (mysqli_connect_error()) {
    exit('Error connecting to the database: ' . mysqli_connect_error());
}

// Check if the form data is set
if (!isset($_POST['email'], $_POST['password'])) {
    exit('Please fill out all fields.');
}

// Validate input
$email = $_POST['email'];
$password = $_POST['password'];

if (empty($email) || empty($password)) {
    exit('email or password cannot be empty.');
}


// Check if the username already exists
$stmt = $conn->prepare("SELECT email FROM login WHERE email = ?");
$stmt->bind_param('s', $email);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    echo 'Username already exists. Please choose another one.';
} else {
    // Prepare statement to insert new user
    $stmt = $conn->prepare("INSERT INTO login (email, password) VALUES (?, ?)");
    $passwordHash = password_hash($password, PASSWORD_DEFAULT);
    $stmt->bind_param('ss', $email, $passwordHash);
    
    if ($stmt->execute()) {
        echo "Successfully registered.";
    } else {
        echo 'Error occurred while registering.';
    }
}

//Verify password
if(password_verify)

$stmt->close();
$conn->close();
?>
