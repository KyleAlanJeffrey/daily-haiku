const nodemailer = require("nodemailer");
const Imap = require("imap-simple");
const { simpleParser } = require("mailparser");
const fs = require("fs");

// Yahoo SMTP and IMAP configuration
const yahooEmail = "your-email@yahoo.com";
const yahooPassword = "your-app-password"; // Use your Yahoo Mail app password

// Create a Nodemailer transporter using Yahoo's SMTP server
const transporter = nodemailer.createTransport({
  service: "yahoo",
  auth: {
    user: yahooEmail,
    pass: yahooPassword,
  },
});

// Function to send an email
function sendEmail() {
  const mailOptions = {
    from: yahooEmail,
    to: "recipient@example.com",
    subject: "Hello from Yahoo Mail",
    text: "This is a test email sent using Yahoo Mail.",
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      return console.log("Error sending email:", error);
    }
    console.log("Email sent:", info.response);
  });
}

// IMAP configuration for reading emails
const imapConfig = {
  imap: {
    user: yahooEmail,
    password: yahooPassword,
    host: "imap.mail.yahoo.com",
    port: 993,
    tls: true,
    authTimeout: 3000,
  },
};

// Function to fetch and save email responses
function fetchEmails() {
  Imap.connect(imapConfig)
    .then((connection) => {
      return connection.openBox("INBOX").then(() => {
        const searchCriteria = ["UNSEEN"];
        const fetchOptions = {
          bodies: ["HEADER.FIELDS (FROM TO SUBJECT DATE)", "TEXT"],
          struct: true,
        };

        return connection
          .search(searchCriteria, fetchOptions)
          .then((messages) => {
            messages.forEach((item) => {
              const all = item.parts.find((part) => part.which === "TEXT");
              const id = item.attributes.uid;

              simpleParser(all.body, (err, mail) => {
                if (err) {
                  console.error("Error parsing email:", err);
                  return;
                }

                const emailData = `
                            From: ${mail.from.text}
                            To: ${mail.to.text}
                            Subject: ${mail.subject}
                            Date: ${mail.date}
                            Message: ${mail.text}
                        `;

                // Save the email response to a local file
                fs.appendFileSync(
                  "emailResponses.txt",
                  emailData + "\n\n",
                  "utf8"
                );
                console.log("Email response saved locally!");
              });
            });
          });
      });
    })
    .catch((err) => {
      console.error("Failed to connect to the email server:", err);
    });
}

// Example usage
sendEmail(); // Send an email
fetchEmails(); // Fetch email responses
