#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email import parser
from email.header import decode_header
from email.utils import parseaddr
from exec_conf import *
from smtp import *

import poplib
import email

pophost = 'pop.163.com'  
smtphost = 'smtp.163.com'

username = 'madlas1977@163.com'  
password = '12345678l'  

pop_inf = {'pophost':'pop.163.com', 'smtphost':'smtp.163.com', 'username':'madlas1977@163.com', 'password':'12345678l', 'act_type':1, 'reply_mail':'madlas1977@aa.cc'}

#获得字符编码方法
def get_charset(message, default="ascii"):
   #Get the message charset
   return message.get_charset()
   return default

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def deal_mail(mail_inf):
	#连接服务器
	popsvr = poplib.POP3(mail_inf['pophost'])
	popsvr.set_debuglevel(0)
	print(popsvr.getwelcome().decode('utf-8'))

	#用户名密码认证
	popsvr.user(mail_inf['username'])
	popsvr.pass_(mail_inf['password'])
	mail_num, mail_size = popsvr.stat()


	#查找新邮件
	trimln_lst = []
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
					hdr, from_addr = parseaddr(message['From'])
					hdr, to_addr = parseaddr(message['To'])


					for part in message.walk():  
						if not part.is_multipart():
							fileName = part.get_filename()  
							contentType = part.get_content_type()  
							charset = get_charset(part)
							
							# 保存附件  
							if fileName:  
								h = email.Header.Header(fileName)
								dh = email.Header.decode_header(h)
								fname = dh[0][0]
								encodeStr = dh[0][1]
								if encodeStr != None:
									if charset == None:
										fname = fname.decode(encodeStr, 'gbk')
									else:
										fname = fname.decode(encodeStr, charset)

								data = part.get_payload(decode=True)  
								with open("recv-bin/%s" % (fname), 'wb') as fEx:
									fEx.write(data)
								build_send_attach(fname, mail_inf['act_type'])

							elif contentType == 'text/plain' or contentType == 'text/html':  
								#保存正文  
								data = part.get_payload(decode=True)  
				
				if mail_inf['act_type'] == 1:
					pass
				elif mail_inf['act_type'] == 2: 
					smtpSendMail(to_addr, from_addr, os.listdir('./send-bin'), mail_inf)
				elif mail_inf['act_type'] == 10: 
					smtpSendMail(to_addr, mail_inf['reply_mail'], os.listdir('./send-bin'), mail_inf)
					pass
					
	rmfp.close()
	popsvr.quit()

	return 0

conf = ConfigParser.ConfigParser()
conf.read("conf/send_ruler.conf")
secs = conf.sections()
for sec in secs:
	if conf.getint(sec, "seg_type") == 99:
		pop_inf['pophost'] = conf.get(sec, 'pop3svr')
		pop_inf['smtphost'] = conf.get(sec, 'smtpsvr')
		pop_inf['username'] = sec
		pop_inf['password'] = conf.get(sec, 'password')
		pop_inf['act_type'] = conf.getint(sec, 'act_type')
		if pop_inf['act_type'] == 10:
			pop_inf['reply_mail'] = conf.get(sec, 'reply_mail')
			
		deal_mail(pop_inf)

