from email.message import EmailMessage
import ssl
import smtplib


def send_mail():
    MAIL_FROM = 'your email id'
    MAIL_PASSWORD = 'your 16 digit password'
    MAIL_TO = 'sender email id'

    subject = "testing 12 12"
    body = """
    I just tried my first email
    """

    em = EmailMessage()
    em['From'] = MAIL_FROM
    em['To'] = MAIL_TO
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(MAIL_FROM, MAIL_PASSWORD)
        smtp.sendmail(MAIL_FROM, MAIL_TO, em.as_string())

    print("mail sent to the system")
