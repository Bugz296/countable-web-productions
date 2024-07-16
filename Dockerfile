# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt

# Copy the start-cron.sh script to the container
COPY /app/scripts/start_cronscript.sh /code/scripts/start_cronscript.sh

# Copy the Python script to the container
COPY /app/scripts/health_check_script.py /code/scripts/health_check_script.py

# Add the cron job
RUN echo "*/1 * * * * /usr/local/bin/python /code/scripts/health_check_script.py >> /var/log/cron.log 2>&1" > /etc/crontabs/root

# Make the start-cron.sh script executable
RUN chmod +x /code/scripts/start_cronscript.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .

# CMD to start both Flask and cron
CMD ["sh", "-c", "flask run --debug & /code/scripts/start_cronscript.sh"]