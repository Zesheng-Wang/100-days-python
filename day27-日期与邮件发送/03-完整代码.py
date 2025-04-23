import os
import smtplib
import threading
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from zoneinfo import ZoneInfo
import pytz


# ====================
# 邮件发送核心模块
# ====================
class EmailSender:
    """安全邮件发送器（支持SSL/TLS）"""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.example.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 465))
        self.username = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PWD")
        self.timeout = 10  # 秒

    def send_email(self, to_addrs, subject, content, attachments=None, html=False):
        """
        发送邮件
        :param to_addrs: 收件人列表
        :param subject: 邮件主题
        :param content: 邮件内容
        :param attachments: 附件路径列表
        :param html: 是否使用HTML格式
        """
        msg = MIMEMultipart()
        msg["From"] = f"自动化系统 <{self.username}>"
        msg["To"] = ", ".join(to_addrs)
        msg["Subject"] = subject
        msg["Date"] = datetime.now(pytz.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

        # 添加正文
        content_type = "html" if html else "plain"
        msg.attach(MIMEText(content, content_type, "utf-8"))

        # 添加附件
        if attachments:
            for file_path in attachments:
                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read())
                    filename = os.path.basename(file_path)
                    part.add_header(
                        "Content-Disposition", "attachment", filename=filename
                    )
                    msg.attach(part)

        try:
            with smtplib.SMTP_SSL(
                self.smtp_server, self.smtp_port, timeout=self.timeout
            ) as server:
                server.login(self.username, self.password)
                server.sendmail(self.username, to_addrs, msg.as_string())
                print(f"邮件成功发送至 {', '.join(to_addrs)}")
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
            raise


# ====================
# 日报生成系统
# ====================
class DailyReporter:
    """智能日报生成器"""

    def __init__(self, timezone="Asia/Shanghai"):
        self.timezone = ZoneInfo(timezone)
        self.template = """<html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
                    .metric {{ background: #f9f9f9; padding: 15px; margin: 10px 0; }}
                    .metric h3 {{ color: #3498db; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{date} 修仙日报</h1>
                </div>
                
                <div class="metrics">
                    <div class="metric">
                        <h3>📊 今日统计</h3>
                        <p>修炼时长: {practice_hours} 小时</p>
                        <p>丹药炼制: {pills_made} 颗</p>
                        <p>心法突破: {breakthroughs} 次</p>
                    </div>
                    
                    <div class="metric">
                        <h3>📅 明日计划</h3>
                        <ul>{next_plan}</ul>
                    </div>
                </div>
            </body>
        </html>
        """

    def generate_report(self, data):
        """生成HTML日报"""
        plan_items = "\n".join([f"<li>{item}</li>" for item in data["next_plan"]])
        return self.template.format(
            date=datetime.now(self.timezone).strftime("%Y-%m-%d"),
            practice_hours=data["practice_hours"],
            pills_made=data["pills_made"],
            breakthroughs=data["breakthroughs"],
            next_plan=plan_items,
        )

    def schedule_daily_report(
        self, send_time="09:00", recipients=None, attachments=None
    ):
        """
        每日定时发送日报
        :param send_time: 发送时间（格式HH:MM）
        :param recipients: 收件人列表
        :param attachments: 附件路径列表
        """

        def get_next_run():
            now = datetime.now(self.timezone)
            target = datetime.strptime(send_time, "%H:%M").time()
            target_dt = now.replace(
                hour=target.hour, minute=target.minute, second=0, microsecond=0
            )
            if now >= target_dt:
                target_dt += timedelta(days=1)
            return target_dt

        def send_task():
            # 生成模拟数据
            report_data = {
                "practice_hours": 6.5,
                "pills_made": 42,
                "breakthroughs": 3,
                "next_plan": [
                    "完成心法第三重修炼",
                    "宗门资源调配会议",
                    "炼丹房设备维护",
                ],
            }

            # 生成并发送邮件
            emailer = EmailSender()
            html_content = self.generate_report(report_data)

            emailer.send_email(
                to_addrs=recipients or [os.getenv("DEFAULT_RECIPIENT")],
                subject=f"修仙日报 {datetime.now().strftime('%Y-%m-%d')}",
                content=html_content,
                attachments=attachments,
                html=True,
            )

            # 重新调度下一次任务
            threading.Timer(
                (get_next_run() - datetime.now(self.timezone)).total_seconds(),
                send_task,
            ).start()

        # 初始启动
        initial_delay = (get_next_run() - datetime.now(self.timezone)).total_seconds()
        threading.Timer(initial_delay, send_task).start()


# ====================
# 使用示例
# ====================
if __name__ == "__main__":
    # 配置环境变量（实际使用时应通过.env文件或系统环境变量配置）
    os.environ.update(
        {
            "SMTP_SERVER": "smtp.xiuxian.com",
            "SMTP_PORT": "465",
            "EMAIL_USER": "system@xiuxian.com",
            "EMAIL_PWD": "your_encrypted_password",
            "DEFAULT_RECIPIENT": "master@xiuxian.com",
        }
    )

    # 初始化日报系统
    reporter = DailyReporter(timezone="Asia/Shanghai")

    # 添加示例附件
    sample_attachments = ["data/修炼记录.pdf", "data/丹药库存.xlsx"]

    # 启动每日9:00自动发送
    reporter.schedule_daily_report(
        send_time="09:00",
        recipients=["master@xiuxian.com", "assistant@xiuxian.com"],
        attachments=sample_attachments,
    )

    # 保持主线程运行
    while True:
        pass
