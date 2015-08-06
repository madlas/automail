import ConfigParser
import string, os, sys

#recv_attach = 'fhj2sys_qdb.dsp'
def build_send_attach(recv_attach):
	conf = ConfigParser.ConfigParser()
	conf.read("conf/send_ruler.conf")

	secs = conf.sections()
	for sec in secs:
		if sec == recv_attach and conf.getint(sec, "seg_type") == 2:
			act_type = conf.getint(sec, "act_type")
			if act_type == 1:
				work_dir = conf.get(sec, "work_dir")
				save_dir = conf.get(sec, "save_dir")
				script_name = conf.get(sec, "script_name")
				send_attach_name = conf.get(sec, "send_attach_name")
				print("cp -f recv-bin/%s %s%s" %(recv_attach, work_dir, save_dir))
				os.popen("cp -f recv-bin/%s %s%s" %(recv_attach, work_dir, save_dir))
				print('>>>>>>>>1\n')
				os.popen("cd %s;./%s; cd -" %(work_dir, script_name))
				print('>>>>>>>>2\n')
				os.popen("cp -f %sfile/send-attach.tar send-bin/%s" %(work_dir, send_attach_name)) 
				print('>>>>>>>>3\n')
				
	
	return 0





