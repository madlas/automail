#coding: utf-8
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.MIMEMultipart import MIMEMultipart
from email.mime.base import MIMEBase 
import re

import os

import email.mime.multipart
from email.MIMEBase import MIMEBase
from email import Encoders

def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr))


def smtpCreMailWithAttach(from_addr, to_addr, subject, msg_files, attach_files):
	from_name = re.split('@', from_addr)[0]
	to_name = re.split('@', to_addr)[0]
	# 邮件对象:
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = Header(subject, 'utf-8').encode()
	msgRoot['From'] = _format_addr('%s<%s>' % (from_name, from_addr))
	msgRoot['To'] = _format_addr('%s<%s>' % (to_name, to_addr))
	msgRoot.preamble = 'This is a multi-part message in MIME format.' 
		
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	for msgfile in msg_files:
			with open('./mail-msg/%s' %(msgfile), 'r') as msgfp:
				Text= msgfp.read()
				if len(Text) > 0:
					if msgfile[-4:] == '.txt':
						#设定纯文本信息
						msgText = MIMEText(Text, 'plain', 'utf-8')
					elif msgfile[-4:] == '.htm':
						#设定HTML信息
						msgText = MIMEText(Text, 'html', 'utf-8')
					msgAlternative.attach(Text)
				
	'''
	# 邮件正文是MIMEText:
	#msgRoot.attach(MIMEText(msg_text, 'plain', 'utf-8'))
	
	for attfile in attach_files:
		att = MIMEBase('application', 'octet-stream')
		att.set_payload(open('send-bin/%s' %(attfile), 'rb').read())
		#att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', attfile))
		att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attfile.decode('utf-8').encode('gbk')))
		encoders.encode_base64(att)
		msgRoot.attach(att)

	'''
	return msgRoot

def smtpSendMail(from_addr, to_addr, subject, msg_lists, attach_lists, svr_inf):
	
	print 'Connect SMTP Server:%s....' %(svr_inf['smtphost'])
	smtpsvr= smtplib.SMTP(svr_inf['smtphost'], 25)
	smtpsvr.set_debuglevel(0)
	print 'Login in!Smtp User:%s...' %(svr_inf['smtp_user'])
	smtpsvr.login(svr_inf['smtp_user'], svr_inf['smtp_pwd'])

	msg = smtpCreMailWithAttach(from_addr, to_addr, subject, msg_lists, attach_lists)
	#smtpsvr.sendmail(from_addr, [to_addr], msg.as_string())
	smtpsvr.quit()
	

	return 0

def sendEmail(fromAdd, toAdd, subject, msg_lists, attach_lists, svr_inf): 

    strFrom = fromAdd
    #strTo = ', '.join(toAdd) 
    strTo = toAdd 
    server = svr_inf.get('smtphost')
    user = svr_inf.get('smtp_user')
    passwd = svr_inf.get('smtp_pwd') 
    if not (server and user and passwd) :
		print 'incomplete login info, exit now'
		return 

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.' 
    # Encapsulate the plain and HTML versions of the message body in an
	# 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative) 
     
    for msgfile in msg_lists:
        with open('./mail-msg/%s' %(msgfile), 'r') as msgfp:
            Text = msgfp.read()
            if len(Text) > 0:
				if msgfile[-4: ] == '.txt':
					#设定纯文本信息
					msgText = MIMEText(Text.decode('gbk').encode('utf-8'), 'plain', 'utf-8')
					msgAlternative.attach(msgText)
				elif msgfile[-4:] == '.htm':
					#设定HTML信息
					msgText = MIMEText(Text.decode('gbk').encode('utf-8'), 'html', 'utf-8')
					msgAlternative.attach(msgText)
    	




    #plainText = 'aaabbbccc'	
    #msgText = MIMEText(plainText, 'plain', 'utf-8')
    #msgAlternative.attach(msgText) 
    #htmlText = '<B>HTML文本2</B>'
    #msgText = MIMEText(htmlText, 'html', 'utf-8')
    #msgAlternative.attach(msgText) 
    	
    for attfile in attach_lists:
		att = MIMEBase('application', 'octet-stream')
		att.set_payload(open('send-bin/%s' %(attfile), 'rb').read())
		#att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', attfile))
		att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attfile.decode('utf-8').encode('gbk')))
		encoders.encode_base64(att)
		msgRoot.attach(att)
	

    smtp = smtplib.SMTP()
    smtp.set_debuglevel(0)
    smtp.connect(server)
    smtp.login(user, passwd)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()

    return 

def sendEmail1(authInfo, fromAdd, toAdd, subject, plainText, htmlText): 
    strFrom = fromAdd
    strTo = ', '.join(toAdd) 
    server = authInfo.get('server')

    user = authInfo.get('user')

    passwd = authInfo.get('password') 
    if not (server and user and passwd) :
		print 'incomplete login info, exit now'
		return 

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.' 
    # Encapsulate the plain and HTML versions of the message body in an
	# 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative) 
    msgText = MIMEText(plainText, 'plain', 'utf-8')
    msgAlternative.attach(msgText) 
    msgText = MIMEText(htmlText, 'html', 'utf-8')
    msgAlternative.attach(msgText) 
    '''
    fp = open('test.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage) 
    '''
    smtp = smtplib.SMTP()
    smtp.set_debuglevel(1)
    smtp.connect(server)
    smtp.login(user, passwd)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()

    return 

def sendmail_use_mutt(to_addr, subject, msg_text, attach_lists):
	
	file_lists = ''
	for att_name in attach_lists:
		file_lists = file_lists + './send-bin/' + att_name + ' '

	print('echo "%s" | mutt -s "%s" %s -a%s' %(msg_text, subject, to_addr, file_lists))
	#os.popen ('echo "%s" | mutt -s "%s" %s -a%s' %(msg_text, subject, to_addr, file_lists))
	return 0

#pop_inf = {'pophost':'pop.163.com', 'smtphost':'smtp.qq.com', 'username':'39728797@qq.com', 'password':'qwerty-123', 'act_type':1, 'reply_mail':'madlas1977@aa.cc', 'allow_list':'', 'smtp_user':'madlas1977@163.com', 'smtp_pwd':'12345678l'}
#smtpSendMail('madlas1977@163.com', '39728797@qq.com', os.listdir('./send-bin'), pop_inf)

'''
if __name__ == '__main__' :

        authInfo = {}

        authInfo['server'] = 'smtp.163.com'

        authInfo['user'] = 'madlas1977'

        authInfo['password'] = '12345678l'

        svrinfo = {}
        svrinfo['smtphost'] = 'smtp.163.com'
        svrinfo['smtp_user'] = 'madlas1977'
        svrinfo['smtp_pwd'] = '12345678l'

        fromAdd = 'madlas1977@163.com'

        #toAdd = ['39728797@qq.com']
        toAdd = '39728797@qq.com'

        #subject = '邮件主题'
        subject = 'test'

        plainText = '这里是普通文本'

        htmlText = '<B>HTML文本</B>'

        sendEmail(fromAdd, toAdd, subject, os.listdir('./mail-msg'), '', svrinfo)
'''
