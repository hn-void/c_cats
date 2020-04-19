import smtplib
import sys
from email.mime.text import MIMEText
from email.utils import formatdate


def create_mail(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


def send_mail(from_addr, password, to_addr, msg):
    try:
        # Login
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(from_addr, password)
        # Send
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        smtpobj.close()
    except Exception:
        print(sys.exc_info())
