import os
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

def send_email(origin, destination, url):
    # Mail parameters
    EMAIL_ADDRESS = "monikagiemela.coding@gmail.com"
    MAIL_PWD = os.environ["MAIL_PWD"]
    RECEPIENTS = ["monikagiemela.coding@gmail.com"]
    ATTACHMENT_PATHS = ["/tmp/flight_prices.csv", "/tmp/screen_shot.png"]

    # Create message object
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ','.join(RECEPIENTS)
    msg['Subject'] = "Ceny Lotów"
    # Mail server parameters
    smtpHost = "smtp.gmail.com"
    smtpPort = 587
    
    mail_content_html = f"Zestawienie cen lotów ze strony <b>{url}</b> dla <b>{origin}-{destination}</b> z dnia <b>{datetime.today()}</b>"
    msg.attach(MIMEText(mail_content_html, 'html'))

    # Create file attachments
    for path in ATTACHMENT_PATHS:
        # Check if file exists
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(path, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        f'attachment; filename="{os.path.basename(path)}"')
        msg.attach(part)
    
    # Send message object as email using smptplib
    s = smtplib.SMTP(smtpHost, smtpPort)
    s.starttls()
    s.login(EMAIL_ADDRESS, MAIL_PWD)
    msgText = msg.as_string()
    sendErrs = s.sendmail(EMAIL_ADDRESS, RECEPIENTS, msgText)
    s.quit()

    # Check if errors occured and handle them accordingly
    if not len(sendErrs.keys()) == 0:
        raise Exception("INFO: Errors occurred while sending email", sendErrs)
    print("INFO: Excution complete...")