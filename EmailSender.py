import os
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

def send_email(origin, destination):
    EMAIL_ADDRESS = "monikagiemela.coding@gmail.com"
    MAIL_PWD = os.environ["MAIL_PWD"]
    RECEPIENTS = ["monisiastella@gmail.com"]
    ATTACHMENT_PATH = ["/tmp/flight_prices.csv"]

    # create message object
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ','.join(RECEPIENTS)
    msg['Subject'] = "Ceny Lotów"
    # mail server parameters
    smtpHost = "smtp.gmail.com"
    smtpPort = 587
    mail_content_html = f"Cześć Tomek, <br/> Przesyłam zestawienie cen lotów dla <b>{origin}-{destination}</b> z dnia <b>{datetime.today()}</b>"
    #msg.attach(MIMEText(mailContentText, 'plain'))
    msg.attach(MIMEText(mail_content_html, 'html'))

    # create file attachments
    for aPath in ATTACHMENT_PATH:
        # check if file exists
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(aPath, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        f'attachment; filename="{os.path.basename(aPath)}"')
        msg.attach(part)
    
    # Send message object as email using smptplib
    s = smtplib.SMTP(smtpHost, smtpPort)
    s.starttls()
    s.login(EMAIL_ADDRESS, MAIL_PWD)
    msgText = msg.as_string()
    sendErrs = s.sendmail(EMAIL_ADDRESS, RECEPIENTS, msgText)
    s.quit()

    # check if errors occured and handle them accordingly
    if not len(sendErrs.keys()) == 0:
        raise Exception("Errors occurred while sending email", sendErrs)
    print("execution complete...")