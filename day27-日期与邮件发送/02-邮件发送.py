import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os


class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.example.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 465))
        self.username = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PWD")

    def send(self, to_addrs, subject, content, attachments=[]):
        msg = MIMEMultipart()
        msg["From"] = f"时光管理系统 <{self.username}>"
        msg["To"] = ", ".join(to_addrs)
        msg["Subject"] = subject

        # HTML正文
        html = f"""<html>
            <body>
                <h1 style="color:#4B8BBE;">{subject}</h1>
                <div>{content}</div>
            </body>
        </html>"""
        msg.attach(MIMEText(html, "html"))

        # 添加附件
        for file in attachments:
            with open(file, "rb") as f:
                part = MIMEApplication(f.read())
                part.add_header(
                    "Content-Disposition", "attachment", filename=os.path.basename(file)
                )
                msg.attach(part)

        # SSL加密发送
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, to_addrs, msg.as_string())
