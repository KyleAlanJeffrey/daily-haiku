# Daily Blog
This repo runs a mail client on my server that sends out once a day. It will then take any response to the email and store it in the daily-response folder and will update the remote repository with the email responses. All of this is so I have a publiclly availble record that i can fetch from anywhere.

## Command
To setup the cronjob run this command and everything should be configured.
```bash
python3 set_cronjob.py
```