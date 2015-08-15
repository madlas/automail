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

#保存文件方法（都是保存在指定的根目录下）
def savefile(filename, data, path):
	try:
		filepath = path + filename
		print 'Saved as ' + filepath
		f = open(filepath, 'wb')
	except:
		print('filename error')
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
					   #fname = fname.decode(encodeStr, 'gbk')
					   fname = fname.decode(encodeStr, 'utf-8')
				   else:
					   fname = fname.decode(encodeStr, charset)
			   data = part.get_payload(decode=True)
			   print('Attachment : ' + fname)
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
		print '\n'
		print 'No : ' + str(number)
		print strfrom
		print strdate
		print strsub
		'''
		print 'Content:'
		print mailContent
		'''
		#保存邮件正文
		if (suffix != None and suffix != '') and (mailContent != None and mailContent != ''):
			savefile(str(number) + suffix, mailContent, mypath)
			number = number + 1
	imapServer.close()
	imapServer.logout()

def LogError(msg):
	
	#fileLog = open("/mnt/ramdisk/automail.log", "a")
	#fileLog = open("./automail.log", "a")
	#print >> fileLog, '<%s> %s' %(time.strftime('%Y-%m-%d %H:%M:%S'), msg)
	#fileLog.close()
	
	print '<%s> %s' %(time.strftime('%Y-%m-%d %H:%M:%S'), msg)

'''	
if __name__ =="__main__":
	#邮件保存在e盘
	mypath ='./'
	print 'begin to get email...'
	getMail('imap.163.com', 'madlasbooks@163.com', 'ipcwblbtxoypdezo', mypath, 993, 1)
	#126邮箱登陆没用ssl
	#getMail('imap.163.com', 'madlasbooks@163.com', 'ipcwblbtxoypdezo', mypath, 143, 0)
	print 'the end of get email.'
'''

pop_inf = {'pophost':'pop.163.com', 'smtphost':'smtp.163.com', 'username':'madlas1977@163.com', 'password':'12345678l', 'act_type':1, 'reply_mail':'madlas1977@aa.cc', 'allow_list':'', 'smtp_user':'', 'smtp_pwd':''}

mypath = './recv-bin/'

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

	LogError('Connect imap server "%s".....' %(pop_inf['pophost']))
	#是否采用ssl
	if ssl == 1:
		imapServer = imaplib.IMAP4_SSL(pop_inf['pophost'], port)
	else:
		imapServer = imaplib.IMAP4(pop_inf['pophost'], port)
	LogError('Login in! User:%s' %(pop_inf['username']))
	imapServer.login(pop_inf['username'], pop_inf['password'])
	LogError('Login in Success')
	#imapServer.select()
	imapServer.select("INBOX", readonly = False)
	#邮件状态设置，新邮件为Unseen
	#Message statues = 'All,Unseen,Seen,Recent,Answered, Flagged'
	resp, items = imapServer.search(None, "Unseen")
	number = 1

	for i in items[0].split():

		#清除临时文件		  
		os.popen("rm -f recv-bin/*")
		os.popen("rm -f send-bin/*")

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

		if pop_inf['act_type'] == 10:
			to_addr = pop_inf['reply_mail']
		else:
			to_addr = from_addr

		strdate = 'Date : ' + msg["Date"]
		subject = email.Header.decode_header(msg["Subject"])
		sub = my_unicode(subject[0][0], subject[0][1])
		strsub = 'Subject : ' + sub
		
		mailContent, suffix = parseEmail(msg, mypath)
		#命令窗体输出邮件基本信息
		LogError('\n')
		LogError('No : ' + str(number))
		LogError(strfrom)
		LogError(strdate)
		LogError(strsub)
		

		#保存邮件正文
		if (suffix != None and suffix != '') and (mailContent != None and mailContent != ''):
			savefile(str(number) + suffix, mailContent, mypath)
			number = number + 1


		attach_list= os.listdir(mypath)
		#附件打包
		for attach in attach_list:
			build_send_attach(attach, pop_inf['act_type'])

		#发送附件
		
		if pop_inf['act_type'] in [2,10]:
			smtpSendMail(pop_inf['smtp_user'], to_addr, os.listdir('./send-bin'), pop_inf)
			LogError('Reply to <%s> file = \n' %(pop_inf['smtp_user']))
			for send_name in os.listdir('./send-bin'):
				LogError(send_name)

	
	imapServer.close()
	imapServer.logout()
	LogError('*******************************************************\n')
			




