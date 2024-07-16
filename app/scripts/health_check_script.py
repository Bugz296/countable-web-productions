import psutil
import os
import requests
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText

# This will load environment variables from the .env file.
load_dotenv()

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

        # Memory usage
        memory = psutil.virtual_memory()
        total_memory = memory.total
        available_memory = memory.available
        memory_usage = (total_memory - available_memory) / total_memory * 100
        
        # Disk usage
        disk_usage = psutil.disk_usage('/')
        response = requests.get(url)

        # Check if response status code is NOT 200
        if response.status_code != 200:

            raise requests.exceptions.RequestException(True)
        elif int(memory_usage) >= 90 or int(disk_usage.percent) >= 95:

            raise requests.exceptions.RequestException()

        return None

    except requests.exceptions.RequestException as is_app_down:
        subject = "APP IS DOWN" if is_app_down else "RUNNING OUT OF MEMORY"
        body = "The app is " + (("down as of " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")) if is_app_down else "running out of memory") + "."
        send_email(subject, body)

# Call function to run script
if __name__ == "__main__":
    run_script(os.getenv('APP_DOCKER_URL'))