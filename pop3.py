import poplib

def connect_pop3(pop3svr, user, passwd):

	server = poplib.POP3(pop3svr)
	server.set_debuglevel(1)
	print(server.getwelcome().decode('utf-8'))

	#用户名密码认证
	server.user(user)
	server.pass_(passwd)
	mail_num, mail_size = server.stat()

	return server, mail_num

def disconnect_pop3(pop3svr):
	pop3svr.quit()
	return None
