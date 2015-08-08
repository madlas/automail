#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email import parser
from email.header import decode_header
from email.utils import parseaddr
from exec_conf import *
from smtp import *

import poplib

pophost = 'pop.163.com'  
smtphost = 'smtp.163.com'

username = 'madlas1977@163.com'  
password = '12345678l'  


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
	
#连接服务器
popsvr = poplib.POP3(pophost)
popsvr.set_debuglevel(1)
print(popsvr.getwelcome().decode('utf-8'))

#用户名密码认证
popsvr.user(username)
popsvr.pass_(password)
mail_num, mail_size = popsvr.stat()


#查找新邮件
trimln_lst = []
#trimln_lst.clear()
with open('conf/recvmail.lst', 'r') as rmfp:
	for line in rmfp.readlines():
		trimln_lst.append(line.strip())

rmfp = open('conf/recvmail.lst', 'a')

for i in range(mail_num):
	mail_uidl = popsvr.uidl(i + 1)
	if mail_uidl[0:3] == b'+OK':
		mail_uidl = mail_uidl[-22:].decode('ascii')
		#如果是新邮件则接收
		#if mail_uidl not in trimln_lst:
		if True:
			rmfp.write('%s\n' %mail_uidl)	
			trimln_lst.append(mail_uidl)

			#获得邮件
			messages = [popsvr.retr(i + 1)]
			# Concat message pieces:  
			messages = ["\n".join(mssg[1]) for mssg in messages]  
					  
			#清除临时文件		  
			os.popen("rm -f recv-bin/*")
			os.popen("rm -f send-bin/*")
			#Parse message intom an email object:  
			# 分析  
			messages = [parser.Parser().parsestr(mssg) for mssg in messages]  
			for message in messages:  
				'''
				value = message.get('From', '')
				if value:
					hdr, addr = parseaddr(value)
					name = decode_str(hdr)
					print('From: %s %s' %(name, addr))

				value = message.get('To', '')
				if value:
					hdr, addr = parseaddr(value)
					name = decode_str(hdr)
					print('To: %s %s' %(name, addr))

				value = message.get('Subject', '')
				if value:
					value = decode_str(value)
					print('Subject: %s' %value)
				'''
				hdr, from_addr = parseaddr(message['From'])
				#name = decode_str(hdr)
				#print('From: %s %s' %(name, addr))
				hdr, to_addr = parseaddr(message['To'])


				for part in message.walk():  
					fileName = part.get_filename()  
					contentType = part.get_content_type()  
					# 保存附件  
					if fileName:  
						data = part.get_payload(decode=True)  
						with open("recv-bin/%s" % (fileName), 'wb') as fEx:
							fEx.write(data)
						build_send_attach(from_addr, fileName)

					elif contentType == 'text/plain' or contentType == 'text/html':  
						#保存正文  
						data = part.get_payload(decode=True)  
						#print >> f, data  

				#f.close()  
			#smtpSendMail(from_addr, to_addr, os.listdir('./send-bin'))
			#sendmail_use_mutt(to_addr, '111', '22222',  os.listdir('./send-bin'))
			reply_to_sender(from_addr, to_addr)

rmfp.close()
popsvr.quit()

