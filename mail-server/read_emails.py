import json
from pathlib import Path
import random
import re
import imaplib
import email
import string
from typing import Dict, Optional
from dotenv import dotenv_values

parent_dir = Path(__file__).resolve().parents[1]
dotenv_path = Path(__file__).resolve().parent / ".env"
config = dotenv_values(
    dotenv_path
)  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

# Email configuration
SMTP_SERVER = "smtp.mail.yahoo.com"
IMAP_SERVER = "imap.mail.yahoo.com"
ALPHABETS = (string.ascii_lowercase, string.ascii_uppercase, string.digits)

EMAIL_ACCOUNT = config["EMAIL"]
PASSWORD = config["PASSWORD"]
CAESAR_SHIFT = config["CAESAR_SHIFT"]


def format_email_body(
    date: str, body: str, json_data: Optional[Dict], encrypt=False
):
    if not json_data:
        json_data = {}

    if "entries" not in json_data:
        json_data["entries"] = []

    if encrypt:
        # Encrypt the email body and add garbage
        body = garbage_generator() + "\n" + caesar(body, int(CAESAR_SHIFT))

    paragraphs = body.split("\n")
    json_data["entries"].append({"date": date, "body": paragraphs})
    return json_data


def garbage_generator():
    return "".join(random.choices(string.ascii_letters, k=25))


# Use a caesar cipher to encode the email body.
def caesar(text: str, step: int):

    def shift(alphabet):
        return alphabet[step:] + alphabet[:step]

    shifted_alphabets = tuple(map(shift, ALPHABETS))
    joined_aphabets = "".join(ALPHABETS)
    joined_shifted_alphabets = "".join(shifted_alphabets)
    table = str.maketrans(joined_aphabets, joined_shifted_alphabets)
    return text.translate(table)


# Function to read emails and save responses locally
def read_emails():
    print("Reading emails...")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select("inbox")

    result, data = mail.search(None, "SEEN")  # Look for unread emails
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
                # Remove quoted text that begins with '>' and remove all \r and \n
                body = (
                    re.sub(r"\n>.*", "", body)
                    .replace("\r", "")
                    .replace("\n", "")
                )

                # Fri, 30 Aug 2024 12:00:43 -0700
                date_str = "-".join(date.split(" ")[1:4])
                # Save email to a local file in json. Check if file content
                # Already exists and append if it does.
                output_file = parent_dir / f"daily-response/{date_str}.txt"
                json_data = {}
                if output_file.exists():
                    print(f"Founding existing entry: {output_file}...")
                    with open(output_file, "r") as f:
                        json_data = json.load(f)

                with open(output_file, "w") as f:
                    json_data = format_email_body(
                        date, body, json_data, encrypt=True
                    )
                    f.write(json.dumps(json_data, indent=4))
                    print(f"Email response saved to {output_file}.")

                filename = output_file.stem
                output_file = parent_dir / "daily-response/metadata.txt"
                if not output_file.exists():
                    output_file.touch()

                update_metadata = False
                with open(output_file, "r") as f:
                    data = " ".join(f.readlines())
                    if filename not in data:
                        update_metadata = True
                if update_metadata:
                    with open(output_file, "a") as f:
                        f.write(f"{filename}\n")
                        print(f"Updated metadata file. with {filename}")

    mail.logout()


read_emails()
