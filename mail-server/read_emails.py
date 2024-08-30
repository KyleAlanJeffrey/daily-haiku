from pathlib import Path
import re
import imaplib
import email
from dotenv import load_dotenv, dotenv_values

parent_dir = Path(__file__).resolve().parents[1]
load_dotenv()  # take environment variables from .env.

config = dotenv_values(
    ".env"
)  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

# Email configuration
SMTP_SERVER = "smtp.mail.yahoo.com"
IMAP_SERVER = "imap.mail.yahoo.com"
EMAIL_ACCOUNT = config["EMAIL"]
PASSWORD = config["PASSWORD"]


# Function to read emails and save responses locally
def read_emails():
    print("Reading emails...")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select("inbox")

    result, data = mail.search(None, "UNSEEN")  # Look for unread emails
    email_ids = data[0].split()

    print(f"Found {len(email_ids)} unread email(s).")
    for email_id in email_ids:
        result, message_data = mail.fetch(email_id, "(RFC822)")
        raw_email = message_data[0][1].decode("utf-8")
        msg = email.message_from_string(raw_email)

        # subject = msg["subject"]
        # from_address = msg["from"]
        date = msg["date"]

        # Process email content
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode("utf-8")
                # Remove quoted text that begins with '>'
                body = re.sub(r"\n>.*", "", body)
                # Fri, 30 Aug 2024 12:00:43 -0700
                date_str = "-".join(date.split(" ")[1:4])
                # Save email to a local file
                output_file = parent_dir / f"daily-response/{date_str}.txt"
                with open(output_file, "a") as f:
                    f.write(f"Date: {date}\n")
                    f.write(f"{body}\n")
                    f.write("\n" + "-" * 50 + "\n")
                print(f"Email response saved to {output_file}.")

    mail.logout()


read_emails()
