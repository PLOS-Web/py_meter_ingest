import smtplib
from time import localtime, strftime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import config

def send_mail(plain_text, subject):

#    s = smtplib.SMTP(config.smtp_server_name, config.smtp_server_port)
    s = smtplib.SMTP(config.smtp_server_name, config.smtp_server_port)
    if not config.simple_email_auth:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(config.email_sender, config.email_password)

    timestamp = strftime("%Y-%m-%d", config.now)
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = config.email_sender
    msg['To'] = ','.join(config.email_to)

    message = MIMEText(plain_text, 'plain', "utf-8")

    msg.attach(message)

    #print msg.as_string()

    s.sendmail(config.email_sender, config.email_to, msg.as_string())
    s.close()
