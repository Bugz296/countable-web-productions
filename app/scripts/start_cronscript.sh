#!/bin/sh

# Start cron
crond

# Keep the container running by tailing the cron log
tail -f /var/log/cron.log