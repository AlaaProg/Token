from tokens import Token
from flask import Flask,request,redirect
from flask_mail import Message,Mail



app = Flask(__name__) 

app.config['MAIL_SERVER']   ='smtp.gmail.com'
app.config['MAIL_PORT']     = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS']  = False
app.config['MAIL_USE_SSL']  = True

token = Token()
mail = Mail(app)

@app.route("/",methods=["GET"])
def index():
  page = """
        <form action="email" method="POST">
          <input type="text" name="email"></input>
          <input type="submit" name="submit" value="subEmail"></input>
        </form>
        """
  return page

@app.route("/email",methods=["POST"])
def SendMail():

	if request.method == "POST":

		sendto = request.form["email"]
		msg = Message(
					"alaa aqeel",
					sender=str(app.config['MAIL_USERNAME']),
					recipients=[sendto],
					body="Hello Boy"
					
				)  
		msg.html="<a href='http://127.0.0.1:5000/%s'>Clik her </a>"%token.dump(sendto)      

		mail.send(msg)

		return "SendMessage to mail"

@app.route("/<string:tkmail>",methods=["GET"])
def toke_chk(tkmail):
	tk = token.load(tkmail)
	if tk != None:
		return "This : "+tk
	return "This Token del <a href='http://127.0.0.1:5000/email'> Try agen </a>"
    	
# 
app.run(debug=True)
