from flask import render_template, Flask, request
import re
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
	acceptedLangage=["bash","netcat","perl","php","python","ruby"]
	ip=""
	ipregex= "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
	port=""
	portregex ="^([1-9][0-9]{0,3}|9000)$"
	langage=""
	server="nc -lvp "
	if request.method == "POST":
		ip=request.form['ip']
		port=request.form['port']
		langage=request.form['lan']
		if re.match(ipregex,ip) and re.match(portregex,port) and langage in acceptedLangage: 
			if langage in acceptedLangage:
				file=open("revshell/"+langage,"r")
				for f in file:
					f= f.replace("[ip]",ip)
					f = f.replace("[port]",port)
				file.close()
				server = server + port
			return render_template('index.html',payload=f,server=server,errors="")
		return render_template('index.html',payload="",server="",errors=error(ip,port,langage))
	else:
		return render_template('index.html')

def error(ip,port,langage):
	error = []
	ipregex= "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
	portregex ="^([1-9][0-9]{0,3}|9000)$"
	acceptedLangage=["bash","netcat","perl","php","python","ruby"]
	if not re.match(ipregex,ip):
		error.append("enter a valid IP address")
	if not re.match(portregex,port):
		error.append("enter a valid port number [1-9999]")
	if not langage in acceptedLangage:
		error.append("use an accepted langage")
	return error