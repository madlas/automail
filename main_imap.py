#-*- encoding: utf-8 -*-
#author : rayment
#CreateDate : 2013-01-24

import imaplib
import email
#设置命令窗口输出使用中文编码
import sys
import re
import time

from exec_conf import *
from smtp import *

reload(sys)
sys.setdefaultencoding('gbk')

def prt_dbg(msg):
	#print >> fileLog, '<%s> %s' %(time.strftime('%Y-%m-%d %H:%M:%S'), msg)
	print '<%s> %s' %(time.strftime('%Y-%m-%d %H:%M:%S'), msg)

#保存文件方法（都是保存在指定的根目录下）
def savefile(filename, data, path):
	try:
		filepath = path + filename
		prt_dbg ('Saved as ' + filepath)
		#os.popen("touch /tmp/%s" %(filename))
		f = open(filepath, 'wb')
	except:
		prt_dbg('filename error')
		f.close()
	f.write(data)
	f.close()
																	   

#字符编码转换方法
def my_unicode(s, encoding):
   if encoding:
	   return unicode(s, encoding)
   else:
	   return unicode(s)


#获得字符编码方法
def get_charset(message, default="ascii"):
   #Get the message charset
   return message.get_charset()
   return default

#解析邮件方法（区分出正文与附件）
def parseEmail(msg, mypath):
   mailContent = None
   contenttype = None
   suffix =None
   for part in msg.walk():
	   if not part.is_multipart():
		   contenttype = part.get_content_type()   
		   filename = part.get_filename()
		   charset = get_charset(part)
		   #是否有附件
		   if filename:
			   h = email.Header.Header(filename)
			   dh = email.Header.decode_header(h)
			   fname = dh[0][0]
			   encodeStr = dh[0][1]
			   if encodeStr != None:
				   if charset == None:
					   fname = fname.decode(encodeStr, 'gbk')
				   else:
					   fname = fname.decode(encodeStr, charset)
			   data = part.get_payload(decode=True)
			   prt_dbg('Attachment : ' + fname)
			   #保存附件
			   if fname != None or fname != '':
				   savefile(fname, data, mypath)            
		   else:
			   if contenttype in ['text/plain']:
				   suffix = '.txt'
			   if contenttype in ['text/html']:
				   suffix = '.htm' 
			   if charset == None:
				   mailContent = part.get_payload(decode=True)
			   else:
				   mailContent = part.get_payload(decode=True).decode(charset)         
   return  (mailContent, suffix)


#获取邮件方法
def getMail(content_conf, diskroot, port = 993, ssl = 1):
	#mypath = diskroot + ':\\'
	mypath = diskroot
	#是否采用ssl
	if ssl == 1:
		imapServer = imaplib.IMAP4_SSL(content_conf['pophost'], port)
	else:
		imapServer = imaplib.IMAP4(content_conf['pophost'], port)
	imapServer.login(content_conf['username'], content_conf['password'])
	imapServer.select()
	#邮件状态设置，新邮件为Unseen
	#Message statues = 'All,Unseen,Seen,Recent,Answered, Flagged'
	resp, items = imapServer.search(None, "Unseen")
	number = 1
	for i in items[0].split():
		#get information of email
		resp, mailData = imapServer.fetch(i, "(RFC822)")   
		mailText = mailData[0][1]
		msg = email.message_from_string(mailText)
		ls = msg["From"].split(' ')
		strfrom = ''
		if(len(ls) == 2):
			fromname = email.Header.decode_header((ls[0]).strip('\"'))
			strfrom = 'From : ' + my_unicode(fromname[0][0], fromname[0][1]) + ls[1]
		else:
			strfrom = 'From : ' + msg["From"]
		strdate = 'Date : ' + msg["Date"]
		subject = email.Header.decode_header(msg["Subject"])
		sub = my_unicode(subject[0][0], subject[0][1])
		strsub = 'Subject : ' + sub
		
		mailContent, suffix = parseEmail(msg, mypath)
		#命令窗体输出邮件基本信息
		prt_dbg ('\n')
		prt_dbg ('No : ' + str(number))
		prt_dbg (strfrom)
		prt_dbg (strdate)
		prt_dbg (strsub)
		'''
		prt_dbg 'Content:'
		prt_dbg mailContent
		'''
		#保存邮件正文
		if (suffix != None and suffix != '') and (mailContent != None and mailContent != ''):
			savefile(str(number) + suffix, mailContent, mypath)
			number = number + 1
	imapServer.close()
	imapServer.logout()


'''	
if __name__ =="__main__":
	#邮件保存在e盘
	mypath ='./'
	prt_dbg 'begin to get email...'
	getMail('imap.163.com', 'madlasbooks@163.com', 'ipcwblbtxoypdezo', mypath, 993, 1)
	#126邮箱登陆没用ssl
	#getMail('imap.163.com', 'madlasbooks@163.com', 'ipcwblbtxoypdezo', mypath, 143, 0)
	prt_dbg 'the end of get email.'
'''

pop_inf = {'pophost':'pop.163.com', 'smtphost':'smtp.163.com', 'username':'madlas1977@163.com', 'password':'12345678l', 'act_type':1, 'reply_mail':'madlas1977@aa.cc', 'allow_list':'', 'smtp_user':'', 'smtp_pwd':''}

recv_bin= './recv-bin/'
send_bin= './send-bin/'
mail_msg = './mail-msg/'
ssl = 1
port = 993

'''
main
'''

conf = ConfigParser.ConfigParser()
conf.read("conf/mail-host.ini")
secs = conf.sections()
for sec in secs:
	if conf.getint(sec, 'enabled') == 0:
		continue
	#读取服务器配置
	pop_inf['pophost'] = conf.get(sec, 'pop3svr')
	pop_inf['smtphost'] = conf.get(sec, 'smtpsvr')
	pop_inf['username'] = sec
	pop_inf['password'] = conf.get(sec, 'password')
	pop_inf['act_type'] = conf.getint(sec, 'act_type')
	pop_inf['smtp_user'] = conf.get(sec, 'smtp_user')
	pop_inf['smtp_pwd'] = conf.get(sec, 'smtp_pwd')
	
	if pop_inf['act_type'] == 10:
		pop_inf['reply_mail'] = conf.get(sec, 'reply_mail')

	pop_inf['allow_list'] = conf.get(sec, 'allow_list')		
	
	allow_list = re.split(',', pop_inf['allow_list'])		

	prt_dbg('Connect imap server "%s".....' %(pop_inf['pophost']))
	#是否采用ssl
	if ssl == 1:
		imapServer = imaplib.IMAP4_SSL(pop_inf['pophost'], port)
	else:
		imapServer = imaplib.IMAP4(pop_inf['pophost'], port)
	prt_dbg('Login in! User:%s' %(pop_inf['username']))
	imapServer.login(pop_inf['username'], pop_inf['password'])
	prt_dbg('Login in Success')
	#imapServer.select()
	imapServer.select("INBOX", readonly = False)
	#邮件状态设置，新邮件为Unseen
	#Message statues = 'All,Unseen,Seen,Recent,Answered, Flagged'
	resp, items = imapServer.search(None, "Unseen")
	number = 1

	for i in items[0].split():

		#清除临时文件		  
		os.popen("rm -f %s*" %(recv_bin))
		os.popen("rm -f %s*" %(send_bin))
		os.popen("rm -f %s*" %(mail_msg))

		#get information of email
		resp, mailData = imapServer.fetch(i, "(RFC822)")   
		imapServer.store(i, '+FLAGS', '\Seen')

		mailText = mailData[0][1]
		msg = email.message_from_string(mailText)
		ls = msg["From"].split(' ')
		strfrom = ''
		if(len(ls) == 2):
			fromname = email.Header.decode_header((ls[0]).strip('\"'))
			strfrom = 'From : ' + my_unicode(fromname[0][0], fromname[0][1]) + ls[1]
			from_addr = ls[1]
		else:
			strfrom = 'From : ' + msg["From"]
			from_addr = msg["From"]
			
		from_addr = from_addr.replace("<", "").replace(">","")
		if from_addr not in allow_list:
			continue


		strdate = 'Date : ' + msg["Date"]
		subject = email.Header.decode_header(msg["Subject"])
		sub = my_unicode(subject[0][0], subject[0][1])
		strsub = 'Subject : ' + sub
		

		if pop_inf['act_type'] == 10:
			to_addr = pop_inf['reply_mail']
		else:
			to_addr = from_addr
			if pop_inf['act_type'] == 2:
				with open('./conf/reply-mail.lst', 'r') as rpmfp:
					for ln in rpmfp.readlines():
						if re.split(',', ln)[0] in sub:
							to_addr = re.split(',', ln)[1]
							break


		mailContent, suffix = parseEmail(msg, recv_bin)
		#命令窗体输出邮件基本信息
		prt_dbg('\n')
		prt_dbg('No : ' + str(number))
		prt_dbg(strfrom)
		prt_dbg(strdate)
		prt_dbg(strsub)
		

		prt_dbg ('Content:')
		prt_dbg (mailContent)

		#保存邮件正文
		if (suffix != None and suffix != '') and (mailContent != None and mailContent != ''):
			savefile(str(number) + suffix, mailContent, mail_msg)
			number = number + 1


		attach_list = os.listdir(recv_bin)
		#附件打包
		for attach in attach_list:
			build_send_attach(attach, pop_inf['act_type'])

		#发送附件
		if pop_inf['act_type'] in [2,10] :#and len(os.listdir(send_bin)) > 0:
				#smtpSendMail(pop_inf['smtp_user'], to_addr, sub, os.listdir(mail_msg), os.listdir(send_bin), pop_inf)
				#sub = '邮件主题'
				sendEmail(pop_inf['smtp_user'], to_addr, 'AutoMail: ' + sub, os.listdir(mail_msg), os.listdir(send_bin), pop_inf)
				prt_dbg('Reply to <%s> file = \n' %(pop_inf['smtp_user']))
				for send_name in os.listdir(send_bin):
					prt_dbg(send_name)

	
	imapServer.close()
	imapServer.logout()
	prt_dbg('*******************************************************\n')
			




