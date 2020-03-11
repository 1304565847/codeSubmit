import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class codeSender(object):
    def __init__(self):
        # 126邮箱账号
        self.sender = "your@126.com"
        # 126邮箱密码
        self.passWord = 'yourpassword'
        #邮件正文是MIMEText:
    
    def send(self, email, code):
        self.s = smtplib.SMTP_SSL("smtp.126.com", 465)
        self.s.set_debuglevel(1)
        self.s.login(self.sender,self.passWord)
        try:
            msg = MIMEMultipart()
            #邮件主题
            msg['Subject'] = "验证码"
            #发送方信息
            msg['From'] = self.sender
            #QQsmtp服务器的端口号为465或587
            msg_content = f"您的验证码是{code}, 请妥善保管"
            msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
            msg['To'] = to = email
            self.s.sendmail(self.sender,to,msg.as_string())
            return "发送成功"
        except smtplib.SMTPException:
            return "发送失败"
