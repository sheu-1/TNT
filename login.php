<?php

// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Start a session (if not already started)
session_start();

// Check if login form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {

  $email = $_POST['email'];
  $password_input = $_POST['password']; // Changed to avoid overwriting the $password variable

  // Connect to the database
  $servername = "localhost";
  $db_username = "root"; // Replace with your database credentials
  $db_password = "";
  $dbname = "new";

  $conn = mysqli_connect($servername, $db_username, $db_password, $dbname);

  // Check connection
  if (mysqli_connect_errno()) {
    exit("Error connecting to database: " . mysqli_connect_error());
  }

  // Prepare statement to fetch user by email
  $stmt = $conn->prepare("SELECT email, password FROM new.sign_up WHERE email = ?");
  if ($stmt === false) {
    exit("Error preparing the statement: " . $conn->error);
  }

  $stmt->bind_param('s', $email);
  $stmt->execute();
  $stmt->store_result();

  // Check if email exists
  if ($stmt->num_rows > 0) {
    $stmt->bind_result($db_email, $db_hashed_password);
    $stmt->fetch();

    // Verify password (compare hashed values)
    if (password_verify($password_input, $db_hashed_password)) {
      // Login successful - create session variables
      $_SESSION['email'] = $email; // You can store additional user data here

      // Redirect to authorized area
      header("Location: dashboard.html");
      //exit();
      echo "foioewg  jtw jfi m "
    } else {
      // Invalid password
      $error_message = "Invalid email or password";
    }
  } else {
    // Email not found
    $error_message = "Invalid email or password";
  }

  $stmt->close();
  $conn->close();
}
?>

<?php
// Display error message if it exists
if (isset($error_message)) {
  echo "<p style='color:red;'>$error_message</p>";
}
?>
