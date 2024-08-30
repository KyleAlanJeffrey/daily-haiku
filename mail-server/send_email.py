import datetime
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from requests import request
from dotenv import dotenv_values

parent_dir = Path(__file__).resolve().parents[1]
dotenv_path = Path(__file__).resolve().parent / ".env"
config = dotenv_values(
    dotenv_path
)  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

# Email configuration
SMTP_SERVER = "smtp.mail.yahoo.com"
IMAP_SERVER = "imap.mail.yahoo.com"
EMAIL_ACCOUNT = config["EMAIL"]
PASSWORD = config["PASSWORD"]


# Send daily email
def send_daily_email():
    # Todays day of the week string
    day = datetime.datetime.today().weekday()
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    day = days[day]

    # grab random quote
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    response = request(method="get", url=url).json()
    useless_fact = response["text"]
    quote_html = f"<blockquote>{useless_fact}</blockquote>"
    html_template = lambda s: f"<!DOCTYPE html><html><body>{s}</body></html>"

    body = html_template(quote_html + "<p>How are you feeling today?</p>")
    recipient_email = "kyle.alan.jeffrey@gmail.com"
    subject = f"{day} Check-in"

    print(f"Sending email for {day}...")
    send_email(recipient_email, subject, body)


# Function to send an email
def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, 587) as server:
        server.starttls(context=context)
        server.login(EMAIL_ACCOUNT, PASSWORD)
        server.send_message(msg)

    print(f"Email sent to {to_address}.")


send_daily_email()
