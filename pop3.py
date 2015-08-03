import poplib

email = 'madlas1977'
password = '12345678l'
pop3svr = 'pop3.163.com'
trimln_lst = []

server = poplib.POP3(pop3svr)
server.set_debuglevel(0)
print(server.getwelcome().decode('utf-8'))


server.user(email)
server.pass_(password)

mail_num, mail_size = server.stat()

trimln_lst.clear()
with open('conf/recvmail.lst', 'r') as rmfp:
	for line in rmfp.readlines():
		trimln_lst.append(line.strip())

rmfp = open('conf/recvmail.lst', 'a')

for i in range(mail_num):
	#print ('uidl:%s' %server.uidl(i+1))
	mail_uidl = server.uidl(i + 1)
	print(mail_uidl[0:4])
	if mail_uidl[0:3] == 'OK+':
		mail_uidl = mail_uidl[-1:-22]
		print('mail_uidl=%s\n' % mail_uidl)
		if mail_uidl not in trimln_lst:
			rmfp.write('%s\n' %mail_uidl.decode('utf-8'))	
			trimln_lst.append(mail_uidl)

rmfp.close()

server.quit()

