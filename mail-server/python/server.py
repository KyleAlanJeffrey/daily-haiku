import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

config = dotenv_values(
    ".env"
)  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

# Email configuration
SMTP_SERVER = "smtp.mail.yahoo.com"
IMAP_SERVER = "imap.mail.yahoo.com"
EMAIL_ACCOUNT = config["EMAIL"]
PASSWORD = config["PASSWORD"]


# Function to send an email
def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, 587) as server:
        server.starttls(context=context)
        server.login(EMAIL_ACCOUNT, PASSWORD)
        server.send_message(msg)

    print(f"Email sent to {to_address}.")


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

        subject = msg["subject"]
        from_address = msg["from"]
        date = msg["date"]

        # Process email content
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode("utf-8")

                # Save email to a local file
                with open("email_responses.txt", "a") as f:
                    f.write(f"From: {from_address}\n")
                    f.write(f"Subject: {subject}\n")
                    f.write(f"Date: {date}\n")
                    f.write(f"Body:\n{body}\n")
                    f.write("\n" + "-" * 50 + "\n")

                print("Email response saved locally.")

    mail.logout()


# Example usage
if __name__ == "__main__":
    recipient_email = "kyle.alan.jeffrey@gmail.com"
    subject = "Test Email from Python using Yahoo"
    body = "This is a test email sent from Python using Yahoo Mail."

    print("Sending email...")
    send_email(recipient_email, subject, body)
    # Wait for responses (adjust the sleep time as needed)
    # time.sleep(30)  # Wait for 30 seconds to allow time for a response

    read_emails()
