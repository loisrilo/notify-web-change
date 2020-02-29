Notify Webs Change
==================

Get notified of tracked web pages. To set it up follow the next steps:

#. fill your settings in the `.env` file.
#. Install all requirements: `pip install -r requirements.txt`.
#. Add a cron job in your machine. For Linux systems you add the following line
   in crontab:

```
$ crontab -e

# Add a similar line at the end.
*/15 * * * * python3 /path/notify-web-change/notify_web_change >> /path/notify-web-change/log/execution.log 2>&1
```
