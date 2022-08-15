import smtplib
import  os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from app import config 
from loguru import logger




def send_email(SUBJECT='subject', FROM='mail@mail.com', TO=['mail@mail.com'], content='any message', file=[]):
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = ','.join(TO)
    msg.add_header('Content-Type', 'text/html')

    html = f'{content}'

    if len(file) > 0:

        for i in file:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(i, "rb").read())
            encoders.encode_base64(part)
            filename = os.path.split(i)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)

    msg.attach(MIMEText(html, 'html'))
    server = smtplib.SMTP_SSL(config.MAIL_SERVER, config.MAIL_PORT)
    server.login(config.USER_MAIL, config.USER_MAIL_PASSWORD)
    server.sendmail(msg['From'], TO, msg.as_string())
    server.quit()
    logger.info(f'message sent to: {msg["To"]}' )