import os
import random
import datetime

# Lists of possible log messages
INFO_MESSAGES = [
    "User logged in successfully",
    "User performed an action",
    "User logged out",
    "Data processed successfully",
    "Configuration updated",
    "User requested data export",
    "New user account created",
    "Session started",
    "Password changed successfully",
    "File uploaded successfully"
]

WARNING_MESSAGES = [
    "Disk space is running low",
    "High memory usage detected",
    "Unexpected behavior observed",
    "Deprecation warning for API usage",
    "Configuration file not found - using defaults",
    "Slow response time from server",
    "User attempted to access restricted area",
    "Possible data inconsistency detected",
    "Network latency observed",
    "User account nearing limit"
]

ERROR_MESSAGES = [
    "Failed to connect to the database",
    "Invalid user credentials",
    "File not found",
    "API request timed out",
    "Insufficient permissions for operation",
    "Data import failed due to format error",
    "Service unavailable",
    "Unexpected exception occurred",
    "Failed to save data",
    "Email sending failed"
]

def generate_log_entry(severity):
    """Generate a log entry based on severity level."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if severity == "INFO":
        message = random.choice(INFO_MESSAGES)
        return f"{timestamp}, INFO: {message}"

    elif severity == "WARNING":
        message = random.choice(WARNING_MESSAGES)
        warning_id = random.randint(1001, 1010)  # Generate unique warning ID
        return f"{timestamp}, WARNING: {message}, (W{warning_id})"

    elif severity == "ERROR":
        message = random.choice(ERROR_MESSAGES)
        error_id = random.randint(2001, 2010)  # Generate unique error ID
        return f"{timestamp}, ERROR: {message}, (E{error_id})"

def generate_log_file(output_folder, file_index, num_lines, error_percentage, warning_percentage):
    """Generate a single log file."""
    log_entries = []
    for _ in range(num_lines):
        rand_num = random.randint(1, 100)
        if rand_num <= error_percentage:
            severity = "ERROR"
        elif rand_num <= error_percentage + warning_percentage:
            severity = "WARNING"
        else:
            severity = "INFO"

        log_entry = generate_log_entry(severity)
        log_entries.append(log_entry)

    log_filename = os.path.join(output_folder, f"log_file_{file_index}.log")
    with open(log_filename, "w") as log_file:
        log_file.write("\n".join(log_entries))

    print(f"Generated {log_filename} with {num_lines} lines.")

def generate_logs(output_folder, num_files, num_lines_per_file, error_percentage, warning_percentage):
    """Generate multiple log files."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_files):
        generate_log_file(output_folder, i + 1, num_lines_per_file, error_percentage, warning_percentage)

if __name__ == "__main__":
    # Parameters
    output_directory = "output_logs"  # Output folder for logs
    number_of_files = 5  # Number of files to generate
    lines_per_file = 2000  # Number of lines per file
    error_percentage = 10  # Percentage of ERROR logs
    warning_percentage = 20  # Percentage of WARNING logs

    generate_logs(output_directory, number_of_files, lines_per_file, error_percentage, warning_percentage)
