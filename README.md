
# Countable Web Productions | Technical

This is a repository for the take home technical test that the Countable Web Production required.




## Run Locally

STEP 1: Clone the project

```bash
  git clone https://github.com/Bugz296/countable-web-productions.git
```

STEP 2: Go to the project directory

```bash
  cd countable-web-productions/
```

STEP 3: Add .env file to parent directory. Details are provided via email.

STEP 4: Update the "EMAIL_TO" in .env to your email or any email address you want the email notification to be sent to.

STEP 5: Install https://hub.docker.com/r/namshi/smtp for email sending. (Skip if already installed)
```bash
  docker pull namshi/smtp
```

STEP 6: Run docker container namshi/smtp. (Skip if already running)
```bash
    docker run -d -p 25:25 namshi/smtp
```

Step 7: Login to gmail using account 👉 jeffreycarlcountablewebproduct@gmail.com. Password is provided via email including the QR code for google authentication for 2-Step Verification. [Login to Gmail](https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ifkv=AdF4I75VMAGqKdZqNlUEMXliAZvPuhh9i8kjlTvQf2vm_Sg5phF6jfh0FcFfsHkZJ4BEHTl97fYr_w&osid=1&passive=1209600&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S721822056%3A1721104524968771&ddm=0)

Step 8: Start the app
```bash
  docker compose up
```

Step 8: Visit http://localhost:8000/


## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
    
## API Reference

#### To simulate app stop.

```http
  GET /simulate_app_stop
```
Wait for every minute, you should be receiving email notifications about the app being down. Only works when email is properly setup and authenticated in local computer.

NOTE: The cronjob that sends email notification runs every minute, you should be receiving email notifications as long as the app is down.

#### To simulate app start / to stop receiving email notification about app being down.

```http
  GET /simulate_app_start
```

#### To simulate app delayed response.

```http
  GET /simulate_app_delay
```
This will make all succeeding responses to have a delayed response of 11 seconds or more.

If this is executed after simulating app stop, the app will automatically start to avoid conflict.

NOTE: The cronjob that sends email notification runs every minute, you should be receiving email notifications as long as the app has delayed responses.

#### To stop delayed response.

```http
  GET /simulate_app_remove_delay
```


## Authors

- [@bugz296](https://github.com/Bugz296)


## Reflections

- Important choices I made when developing the app.
    - Improved directory structure. I implemented the folder structure based on my experience working with applications using the MVC architecture. I find it most needed and important for codes to be easily found and reengineered if there's a structure being followed.
    - Right libraries. There are many libraries available out there, it is important to use light weight libraries especially if you only need around 30% functionality from it.
    - Applied SOLID, YAGNI, KISS and DRY coding principles.
    - Check and balance. I created a function that will catch delayed responses already in the API itself and another one in the script. This will ensure reliability of the monitoring system.
    - Modularized. It is important for ground up application to have separate folders based on functionality because it tends to be complex in the long run. I have to create folders for controllers, models, middlewares, and helpers to easily handle integration in the future.
    - Documentation. As a team player, I wanted also others to easily understand how I worked on things. It shrinks the learning curve for new members of the team.
    - Security. This is important since once a system is compromised it is an additional task for the team to rebuild the system security. For this app, I made sure all sensitive information is hidden from public.

- Assumptions / Recommendation
    - What I recommend would be separating the container for the app and the script for monitoring computer health. For large applications, if the script is being run on a device same as the application. ie. Observing yourself with your eyes / from within. It is also efficient and effective if there's someone not within the system who would check. Checking the health status with a third party perspective to be short.
    - When I worked on this, I read first all the instructions. As I read, I came up with how would I be implementing this. I have already worked on things like this in the past as a hobby, so I knew how do I start. For me, I believe that "A problem well-stated is half-solved" and a problem you know where to start is 75% solved.

Feel free to email me for any assistance. Thank you.
