import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_alert(subject, content):

    mail_host = 'smtp.163.com'
    mail_user = 'nyadealert@163.com'
    mail_pass = '199723wwq'

    sender = mail_user
    receivers = mail_user

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = _format_addr('网易云音乐提醒!<%s>' %'sender@163.com')
    message['To'] = _format_addr('DNyade<%s>' %'receiver@163.com')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp = smtplib.SMTP_SSL()
        smtp.connect(mail_host, 465)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, receivers, message.as_string())
        print('success')
    except smtplib.SMTPException:
        print('error')

if __name__ == '__main__':
    send_alert('Test','Test')