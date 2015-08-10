#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.MIMEMultipart import MIMEMultipart

import smtplib
import os

def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = 'madlas1977@163.com'
password = '12345678l'
to_addr = '39728797@qq.com'
smtp_server = 'smtp.163.com'

def smtpCreMailWithAttach(from_addr, to_addr, subject, msg_text, attach_files):
	# 邮件对象:
	msgRoot = MIMEMultipart()
	msgRoot['From'] = _format_addr('Automail <%s>' % from_addr)
	msgRoot['To'] = _format_addr('replay <%s>' % to_addr)
	msgRoot['Subject'] = Header(subject, 'utf-8').encode()

	# 邮件正文是MIMEText:
	msgRoot.attach(MIMEText(msg_text, 'plain', 'utf-8'))

	for attfile in attach_files:
		att = MIMEText(open('send-bin/%s' %(attfile), 'rb').read(), 'base64', 'utf-8')  
		att["Content-Type"] = 'application/octet-stream'  
		att["Content-Disposition"] = 'attachment; filename="%s"' % (attfile)
		msgRoot.attach(att) 

	return msgRoot

def smtpSendMail(from_addr, to_addr, attach_lists, svr_inf):
	smtpsvr= smtplib.SMTP(svr_inf['smtphost'], 25)
	smtpsvr.set_debuglevel(1)
	smtpsvr.login(svr_inf['username'], svr_inf['password'])

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
