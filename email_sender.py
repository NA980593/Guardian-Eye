# from flask_mail import Mail, Message

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'guardianeyeco@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Circu$508Kyd' #make this an env variable
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

# mail = Mail(app)

# @app.route("/send_email", methods=['POST'])
# def send_email():
#    msg = Message('Hello', sender = 'guardianeyeco@gmail.com', recipients = ['kylezanderson@gmail.com'])
#    msg.body = "This is the email body"
#    mail.send(msg)
#    return "Sent"

import smtplib
import ssl
import smtplib
from email.message import EmailMessage


def send_email(message,message_sender_name):
   # # creates SMTP session
   # s = smtplib.SMTP('smtp.gmail.com', 465)
   # # start TLS for security
   # s.starttls()
   # # Authentication
   # s.login("guardianeyeco@gmail.com", "Circu$508Kyd")
   # # message to be sent
   # message = "Test message"
   # # sending the mail
   # s.sendmail("guardianeyeco@gmail.com", "kylezanderson@gmail.com", message)
   # # terminating the session
   # s.quit()

   smtpserver = "smtp.gmail.com"
   port = 465
   senderemail = "guardianeyeco@gmail.com"
   receiveremail = "kylezanderson54@gmail.com"
   password = os.getenv('EMAIL_PASS')
   
   subject = "Suspicious message alert"
   body = "Your child Ben has received the following suspicious message from the user "+message_sender_name+":\n"+message

   em=EmailMessage() 
   em['From'] = senderemail
   em['to'] = receiveremail
   em['Subject'] = subject
   em.set_content(body)
   with smtplib.SMTP_SSL(smtpserver, port, context=ssl.create_default_context()) as server: # Context created directly here
      server.login(senderemail, password)
      server.sendmail(senderemail, receiveremail, em.as_string())
   print("email sent.")