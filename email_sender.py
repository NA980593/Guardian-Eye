from flask_mail import Mail, Message

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'guardianeyeco@gmail.com'
app.config['MAIL_PASSWORD'] = '' #make this an env variable
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/send_email", methods=['POST'])
def send_email():
   msg = Message('Hello', sender = 'guardianeyeco@gmail.com', recipients = ['kylezanderson@gmail.com'])
   msg.body = "This is the email body"
   mail.send(msg)
   return "Sent"

