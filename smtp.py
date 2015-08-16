#coding: utf-8
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.MIMEMultipart import MIMEMultipart
from email.mime.base import MIMEBase 

import os

import email.mime.multipart
from email.MIMEBase import MIMEBase
from email import Encoders

def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr))


def smtpCreMailWithAttach(from_addr, to_addr, subject, msg_text, attach_files):
	# 邮件对象:
	msgRoot = MIMEMultipart()
	msgRoot['From'] = _format_addr('Automail <%s>' % from_addr)
	msgRoot['To'] = _format_addr('replay <%s>' % to_addr)
	msgRoot['Subject'] = Header(subject, 'utf-8').encode()

	# 邮件正文是MIMEText:
	msgRoot.attach(MIMEText(msg_text, 'plain', 'utf-8'))

	for attfile in attach_files:
		att = MIMEBase('application', 'octet-stream')
		att.set_payload(open('send-bin/%s' %(attfile), 'rb').read())
		#att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', attfile))
		att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attfile.decode('utf-8').encode('gbk')))
		encoders.encode_base64(att)
		msgRoot.attach(att)

	return msgRoot

def smtpSendMail(from_addr, to_addr, attach_lists, svr_inf):
	print 'Connect SMTP Server:%s....' %(svr_inf['smtphost'])
	smtpsvr= smtplib.SMTP(svr_inf['smtphost'], 25)
	smtpsvr.set_debuglevel(0)
	print 'Login in!Smtp User:%s...' %(svr_inf['smtp_user'])
	smtpsvr.login(svr_inf['smtp_user'], svr_inf['smtp_pwd'])

	msg = smtpCreMailWithAttach(from_addr, to_addr, '1234', '2234', attach_lists)
	smtpsvr.sendmail(from_addr, [to_addr], msg.as_string())
	smtpsvr.quit()

	return 0
def sendmail_use_mutt(to_addr, subject, msg_text, attach_lists):
	
	file_lists = ''
	for att_name in attach_lists:
		file_lists = file_lists + './send-bin/' + att_name + ' '

	print('echo "%s" | mutt -s "%s" %s -a%s' %(msg_text, subject, to_addr, file_lists))
	#os.popen ('echo "%s" | mutt -s "%s" %s -a%s' %(msg_text, subject, to_addr, file_lists))
	return 0

#pop_inf = {'pophost':'pop.163.com', 'smtphost':'smtp.qq.com', 'username':'39728797@qq.com', 'password':'qwerty-123', 'act_type':1, 'reply_mail':'madlas1977@aa.cc', 'allow_list':'', 'smtp_user':'madlas1977@163.com', 'smtp_pwd':'12345678l'}
#smtpSendMail('madlas1977@163.com', '39728797@qq.com', os.listdir('./send-bin'), pop_inf)



