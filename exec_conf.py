# -*- coding: utf-8 -*-

import ConfigParser
import string, os, sys

from smtp import*

#recv_attach = 'fhj2sys_qdb.dsp'
def build_send_attach(from_addr, attach_file):
	conf = ConfigParser.ConfigParser()
	conf.read("conf/send_ruler.conf")

	secs = conf.sections()
	addr_act_type = -1
	for sec in secs:
		if sec == from_addr and conf.getint(sec, "seg_type") == 1:
			addr_act_type = conf.getint(sec, "act_type")
			break
	if addr_act_type < 0:
		return -1
	#只上传	
	if addr_act_type == 1:		
		for sec in secs:
			if sec == attach_file and conf.getint(sec, "seg_type") == 2:
				work_dir = conf.get(sec, "work_dir")
				save_dir = conf.get(sec, "save_dir")
				send_attach_name = conf.get(sec, "send_attach_name")
				os.popen("cp -f recv-bin/%s %s%s" %(attach_file, work_dir, save_dir))
	#上传以后发送
	elif addr_act_type == 2:
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
	elif addr_act_type == 3:
		os.popen("cp -f recv-bin/* send-bin/*")
	else:
		pass


	return 0

def reply_to_sender(from_adr, to_adr):
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
				smtpSendMail(to_adr, from_adr, os.listdir('./send-bin'))
			elif addr_act_type == 3:
				#回复指定地址
				from_adr = conf.get(sec, "send_mail")
				smtpSendMail(to_adr, from_adr, os.listdir('./send-bin'))
			else:
				pass

			break		
	return 0




	





