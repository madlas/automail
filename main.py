#!/usr/bin/env python  
# coding=utf-8  
# Python 2.7.3  
# 获取邮件内容  
import poplib
from email import parser


def build_send_attach(recv_attach_fname)
	return

host = 'pop.163.com'  
username = 'xxxxxxxx@163.com'  
password = 'xxxxxxxx'  

#连接服务器
server = poplib.POP3(host)
server.set_debuglevel(1)
print(server.getwelcome().decode('utf-8'))

#用户名密码认证
server.user(username)
server.pass_(password)
mail_num, mail_size = server.stat()


#查找新邮件
trimln_lst = []
#trimln_lst.clear()
with open('conf/recvmail.lst', 'r') as rmfp:
	for line in rmfp.readlines():
		trimln_lst.append(line.strip())

rmfp = open('conf/recvmail.lst', 'a')

for i in range(mail_num):
	mail_uidl = server.uidl(i + 1)
	if mail_uidl[0:3] == b'+OK':
		mail_uidl = mail_uidl[-22:].decode('ascii')
		#如果是新邮件则接收
		if mail_uidl not in trimln_lst:
			rmfp.write('%s\n' %mail_uidl)	
			trimln_lst.append(mail_uidl)
			#获得邮件
			messages = [server.retr(i + 1)]
			# Concat message pieces:  
			messages = ["\n".join(mssg[1]) for mssg in messages]  
					  
			#Parse message intom an email object:  
			# 分析  
			messages = [parser.Parser().parsestr(mssg) for mssg in messages]  
			i = 0  
			for message in messages:  
				i = i + 1  
				mailName = "mail%d.%s" % (i, message["Subject"])  
				f = open(mailName + '.log', 'w');  
				print >> f, "Date: ", message["Date"]  
				print >> f, "From: ", message["From"]  
				print >> f, "To: ", message["To"]  
				print >> f, "Subject: ", message["Subject"]  
				print >> f, "Data: "  
				j = 0  
				for part in message.walk():  
					j = j + 1  
					fileName = part.get_filename()  
					contentType = part.get_content_type()  
					# 保存附件  
					if fileName:  
						data = part.get_payload(decode=True)  
						with open("recv-bin/%s" % (fileName), 'wb') as fEx:
							fEx.write(data)
						build_send_attach(fileName)

					elif contentType == 'text/plain' or contentType == 'text/html':  
						#保存正文  
						data = part.get_payload(decode=True)  
						print >> f, data  

				f.close()  

rmfp.close()
server.quit()

