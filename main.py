from pop3 import *

trimln_lst = []
server, mail_num = connect_pop3('pop3.163.com', 'madlas1977', '12345678l')

trimln_lst.clear()
with open('conf/recvmail.lst', 'r') as rmfp:
	for line in rmfp.readlines():
		trimln_lst.append(line.strip())

rmfp = open('conf/recvmail.lst', 'a')

for i in range(mail_num):
	mail_uidl = server.uidl(i + 1)
	if mail_uidl[0:3] == b'+OK':
		mail_uidl = mail_uidl[-22:].decode('ascii')
		print(mail_uidl)
		print(trimln_lst)
		if mail_uidl not in trimln_lst:
			rmfp.write('%s\n' %mail_uidl)	
			trimln_lst.append(mail_uidl)

rmfp.close()
disconnect_pop3(server)

