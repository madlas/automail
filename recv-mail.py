import poplib

#连接pop3服务器
email = 'madlas1977'
password = '12345678l1'
pop3svr = 'pop3.163.com'
trimln_lst = []

server = poplib.POP3(pop3svr)
server.set_debuglevel(1)
print(server.getwelcome().decode('utf-8'))

#用户名密码认证
server.user(email)
server.pass_(password)
print('>>>>>>>>>>>>>>>>')
#捡取新邮件
mail_num, mail_size = server.stat()

trimln_lst.clear()
with open('conf/recvmail.lst', 'r') as rmfp:
	for line in rmfp.readlines():
		trimln_lst.append(line.strip())

rmfp = open('conf/recvmail.lst', 'a')

for i in range(mail_num):
	mail_uidl = server.uidl(i + 1)
	if mail_uidl[0:3] == b'+OK':
		mail_uidl = mail_uidl[-22:]
		if mail_uidl not in trimln_lst:
			rmfp.write('%s\n' %mail_uidl.decode('utf-8'))	
			trimln_lst.append(mail_uidl)

rmfp.close()

server.quit()

