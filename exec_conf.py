# -*- coding: utf-8 -*-

import ConfigParser
import string, os, sys

from smtp import*

def build_send_attach(attach_file, act_type):
	conf = ConfigParser.ConfigParser()
	conf.read("conf/attach-build.ini")

	secs = conf.sections()
	#只上传	
	if act_type == 1:		
		for sec in secs:
			if sec == attach_file and conf.getint(sec, "seg_type") == 2:
				work_dir = conf.get(sec, "work_dir")
				save_dir = conf.get(sec, "save_dir")
				send_attach_name = conf.get(sec, "send_attach_name")
				os.popen("cp -f recv-bin/%s %s%s" %(attach_file, work_dir, save_dir))
	#上传以后发送
	elif act_type == 2:
		for sec in secs:
			if sec == attach_file and conf.getint(sec, "seg_type") == 2:
				work_dir = conf.get(sec, "work_dir")
				save_dir = conf.get(sec, "save_dir")
				script_name = conf.get(sec, "script_name")
				send_attach_name = conf.get(sec, "send_attach_name")
				os.popen("cp -f recv-bin/%s %s%s" %(attach_file, work_dir, save_dir))
				os.popen("cd %s;./%s; cd -" %(work_dir, script_name))
				os.popen("cp -f %sfile/send-attach.tar send-bin/%s" %(work_dir, send_attach_name)) 
	#只转发
	elif act_type == 10:
		os.popen("cp -f recv-bin/* send-bin")
	else:
		pass


	return 0

def reply_to_sender(from_adr, to_adr, mailsvr_inf):
	conf = ConfigParser.ConfigParser()
	conf.read("conf/send_ruler.conf")
	secs = conf.sections()
	print secs, from_adr
	for sec in secs:
		if sec == from_adr and conf.getint(sec, "seg_type") == 1:
			addr_act_type = conf.getint(sec, "act_type")
			if addr_act_type == 1:
				#只上传	
				pass
			elif addr_act_type == 2: 
				#回复发件人
				print(to_adr, from_adr)
				smtpSendMail(to_adr, from_adr, os.listdir('./send-bin'), mailsvr_inf)
			elif addr_act_type == 3:
				#回复指定地址
				from_adr = conf.get(sec, "send_mail")
				smtpSendMail(to_adr, from_adr, os.listdir('./send-bin'), mailsvr_inf)
			else:
				pass

			break		
	return 0




	





