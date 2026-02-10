import smtplib
import time
from email.message import EmailMessage

def send_email(recipient_email, email_subject, text_to_insert):
    # sender_email = st.secrets['my_email']['email']   # no-reply@media-meter.com
    # password = st.secrets['my_email']['pass']        # M365 mailbox password

    sender_email = "no-reply@media-meter.com"
    password = "PrSM6-wn"

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = email_subject
    msg.set_content(text_to_insert)

    try:
        # with st.spinner("Sending email..."):
        with smtplib.SMTP("smtp.office365.com", 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            server.send_message(msg)

        time.sleep(2)

        # st.success(f"Successfully sent email to {recipient_email}")
        print(f"Successfully sent email to {recipient_email}")

    except Exception as e:
        # st.error(f"Failed to send email:\n{repr(e)}")
        print(f"Failed to send email:\n{repr(e)}")


send_email("rialyn.santos@media-meter.com", "Test Email Subject", "This is a test email content.")