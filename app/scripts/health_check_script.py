import psutil
import os
import requests
import smtplib
import time
from dotenv import load_dotenv
from email.mime.text import MIMEText

# This will load environment variables from the .env file.
load_dotenv()

# This can be saved to database or into a different file. I added this here just for now.
errors = {
    "request_timeout": "responding so slow.",
    "internal_error": "not responding.",
    "out_of_memory": "running out of memory. Upgraded!"
}

# Function for sending emails.
def send_email(subject, body, to_email = os.getenv('EMAIL_TO')):

    # Get configuration from .env file.
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')

    # Create post data.
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = to_email

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to secure
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(smtp_username, [to_email], msg.as_string())

        # Close the connection to the SMTP server
        server.quit()

        print(f'Email sent successfully to {to_email}')

    except Exception as e:
        print(f'Failed to send email: {e}')


# Run script
def run_script(url):
    try:

        start_time = time.time()

        # Memory usage
        memory = psutil.virtual_memory()
        total_memory = memory.total
        available_memory = memory.available
        memory_usage = (total_memory - available_memory) / total_memory * 100
        
        # Disk usage
        disk_usage = psutil.disk_usage('/')
        response = requests.get(url)

        end_time = time.time()
        elapsed_time = int(end_time - start_time)

        # Cheeck if status code is 408 or elapsed time is more than 10 seconds.
        if response.status_code == 408 or elapsed_time > 10:
    
            raise requests.exceptions.RequestException("request_timeout")

        # Check if response status code is NOT 200.
        elif response.status_code != 200:

            raise requests.exceptions.RequestException("internal_error")

        # Check if memory usage is greater than 90% or disk usage is more than 95%.
        elif int(memory_usage) >= 90 or int(disk_usage.percent) >= 95:

            raise requests.exceptions.RequestException("out_of_memory")

        return None

    except requests.exceptions.RequestException as error:
        subject = "APP WARNING!"
        body = "The app is " + errors[str(error)]
        send_email(subject, body)

# Call function to run script
if __name__ == "__main__":
    run_script(os.getenv('APP_DOCKER_URL'))