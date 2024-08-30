from pathlib import Path
import subprocess

curr_dir = Path(__file__).resolve().parents[0]


def set_cron_job(cron_freq: str, script_path: str, python_path: str):
    # Define the cron job command
    cron_command = f"{cron_freq} {python_path} {script_path}"

    # Use subprocess to add the cron job
    process = subprocess.Popen(
        ["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        # If crontab exists, append the new job
        current_cron = stdout.decode("utf-8")
        if cron_command not in current_cron:
            new_cron = current_cron + cron_command + "\n"
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.communicate(input=new_cron.encode("utf-8"))
            print("Cron job added successfully.")
        else:
            print("Cron job already exists.")
    else:
        # If no crontab exists, create a new one
        process = subprocess.Popen(
            ["crontab", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.communicate(input=(cron_command + "\n").encode("utf-8"))
        print("Cron job created successfully.")


# Set daily cron job to send an email
cron_freq = "*/1 * * * *"  # Every minute
daily_freq = "0 9 * * *"  # 9:00 AM daily
ten_min_freq = "*/10 * * * *"  # Every 10 minutes
set_cron_job(
    cron_freq=cron_freq,
    script_path=str(curr_dir / "send_email.py"),
    python_path=str(curr_dir / "venv/bin/python"),
)

# Set hourly cron job to read emails
set_cron_job(
    cron_freq=cron_freq,
    script_path=str(curr_dir / "read_emails.py"),
    python_path=str(curr_dir / "venv/bin/python"),
)
