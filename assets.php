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
if (!isset($_POST['firstname'], $_POST['secondname'], $_POST['email'], $_POST['password'], $_POST['confirmpassword'])) {
    exit('Please fill out all fields.');
}

// Validate input
$firstname = $_POST['firstname'];
$secondname = $_POST['secondname'];
$email = $_POST['email'];
$password = $_POST['password'];
$confirmpassword = $_POST['confirmpassword'];

if (empty($firstname) || empty($secondname) || empty($email) || empty($password) || empty($confirmpassword)) {
    exit('Fields cannot be empty.');
}

// Check if passwords match
if ($password !== $confirmpassword) {
    exit('Passwords do not match.');
}

// Check if the email already exists
$stmt = $conn->prepare("SELECT email FROM sign_up WHERE email = ?");
$stmt->bind_param('s', $email);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    echo 'User already exists. Please choose another one.';
} else {
    // Prepare statement to insert new user
    $stmt = $conn->prepare("INSERT INTO sign_up (firstname, secondname, email, password) VALUES (?, ?, ?, ?)");
    $passwordHash = password_hash($password, PASSWORD_DEFAULT);
    $stmt->bind_param('ssss', $firstname, $secondname, $email, $passwordHash);
    
    if ($stmt->execute()) {
        echo "Successfully registered.";
    } else {
        echo 'Error occurred while registering.';
    }
}

$stmt->close();
$conn->close();
?>
