import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    def send_email(self,to,msg,subject="Flux Automation"):
        message = MIMEText(msg)
        message['Subject'] = subject
        message['From'] = self.email
        message['To'] = to
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(message)
            server.quit()
            return {'Output': f'The Email has been sent to {to}'}
        except Exception as e:
            return {'Error': f'The Email could not be sent to {to}. Error: {str(e)}'}
    def send_email_with_attachment(self,to,msg,attachments_path,subject="Flux Automation"):
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.email
        message['To'] = to
        message.attach(MIMEText(msg, 'plain'))
        try:
            for attachment_path in attachments_path:
                with open(attachment_path,'rb') as f:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(f.read())
                encoders.encode_base64(attachment)
                attachment.add_header("Content-Disposition",f"attachment; filename= {os.path.basename(attachment_path)}")
                message.attach(attachment)
        except Exception as e:
            return {'Error': f'File not found: {attachment_path} or the issuer might be the following error. Error: {str(e)}'}
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(message)
            server.quit()
            return {'Output': f'The Email has been sent to {to}'}
        except Exception as e:
            return {'Error': f'The Email could not be sent to {to}. Error: {str(e)}'}