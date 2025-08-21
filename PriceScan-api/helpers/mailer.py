
# import smtplib
# import time
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# import pdfkit
# from flask import make_response, render_template

# from config.constant import *

# gmail_user = EMAIL_USER
# gmail_password = EMAIL_PASSWORD

# def send_mailer(username:any, email:any, user_validation_token:any):
#     fromaddr = gmail_user
#     toaddr = email
#     subject = 'EMAIL VERIFICATION REQUIRED'
#     body = render_template("validation_email.html", username=username, user_validation_token=user_validation_token)

#     msg = MIMEMultipart()
#     # storing the senders email address
#     msg['From'] = fromaddr
#     # storing the receivers email address 
#     msg['To'] = ", ".join(toaddr)
#     # storing the subject 
#     msg['Subject'] = subject
#     # string to store the body of the mail
#     body = body
#     # attach the body with the msg instance
#     msg.attach(MIMEText(body,'html', 'utf-8'))
    
#     # open the file to be sent 
#     filename = "keletick.png"
#     attachment = open("static/assets/logo.png", "rb")
    
#     # instance of MIMEBase and named as p
#     p = MIMEBase('application', 'octet-stream')
#     # To change the payload into encoded form
#     p.set_payload((attachment).read())
#     # encode into base64
#     encoders.encode_base64(p)
#     p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#     # attach the instance 'p' to instance 'msg'
#     msg.attach(p)
    
#     # creates SMTP session
#     # s = smtplib.SMTP('smtp.gmail.com', 587)
#     s = smtplib.SMTP('smtppro.zoho.in', 587)

    
#     # start TLS for security
#     s.starttls()
    
#     # Authentication
#     s.login(fromaddr, gmail_password)
    
#     # Converts the Multipart msg into a string
#     text = msg.as_string()
    
#     # sending the mail
#     s.sendmail(fromaddr, toaddr, text)
    
#     # terminating the session
#     s.quit()

# def send_welcome_mailer(username:any, email):
#     fromaddr = gmail_user
#     toaddr = email
#     subject = 'Welcome to Keletick! 🎉 Getting started is easy'
#     body = render_template("welcome_email.html", username=username)

#     msg = MIMEMultipart()
#     # storing the senders email address
#     msg['From'] = fromaddr
#     # storing the receivers email address 
#     msg['To'] = ", ".join(toaddr)
#     # storing the subject 
#     msg['Subject'] = subject
#     # string to store the body of the mail
#     body = body
#     # attach the body with the msg instance
#     msg.attach(MIMEText(body,'html', 'utf-8'))
    
#     # open the file to be sent 
#     filename = "keletick.png"
#     attachment = open("static/assets/logo.png", "rb")
    
#     # instance of MIMEBase and named as p
#     p = MIMEBase('application', 'octet-stream')
#     # To change the payload into encoded form
#     p.set_payload((attachment).read())
#     # encode into base64
#     encoders.encode_base64(p)
#     p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#     # attach the instance 'p' to instance 'msg'
#     msg.attach(p)
    
#     # creates SMTP session
#     # s = smtplib.SMTP('smtp.gmail.com', 587)
#     s = smtplib.SMTP('smtppro.zoho.in', 587)

    
#     # start TLS for security
#     s.starttls()
    
#     # Authentication
#     s.login(fromaddr, gmail_password)
    
#     # Converts the Multipart msg into a string
#     text = msg.as_string()
    
#     # sending the mail
#     s.sendmail(fromaddr, toaddr, text)
    
#     # terminating the session
#     s.quit()
    
# def send_receipt(username:any, invoice:str, order_details:any, qr_code:any, email:any):
#     fromaddr = gmail_user
#     toaddr = email
#     subject = 'Customer Invoice'+ str(invoice)
#     body = render_template("receipt.html", order_details=order_details, qr_code=qr_code)

#     msg = MIMEMultipart()
#     # storing the senders email address
#     msg['From'] = fromaddr
#     # storing the receivers email address 
#     msg['To'] = ", ".join(toaddr)
#     # storing the subject 
#     msg['Subject'] = subject
#     # string to store the body of the mail
#     body = body
#     # attach the body with the msg instance
#     msg.attach(MIMEText(body,'html', 'utf-8'))
    
#     """ render template to pdf in order to send """
#     config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
#     css = ''
#     pdf = pdfkit.from_string(body, False,configuration=config, css=css, options={"enable-local-file-access": ""}) 
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    
#     with open('output.pdf', 'wb') as output:
#         output.write(pdf)
    
#     # open the file to be sent 
#     filename = "ticket #"+str(invoice)+".pdf"
#     attachment = open("output.pdf", "rb")
#     """ render template to pdf in order to send """
    
#     # instance of MIMEBase and named as p
#     p = MIMEBase('application', 'octet-stream')
#     # To change the payload into encoded form
#     p.set_payload((attachment).read())
#     # encode into base64
#     encoders.encode_base64(p)
#     p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#     # attach the instance 'p' to instance 'msg'
#     msg.attach(p)
    
#     # creates SMTP session
#     s = smtplib.SMTP('smtppro.zoho.in', 587)
#     # s = smtplib.SMTP('smtp.office365.com', 587)
    
#     # start TLS for security
#     s.starttls()
    
#     # Authentication
#     s.login(fromaddr, gmail_password)
    
#     # Converts the Multipart msg into a string
#     text = msg.as_string()
    
#     # sending the mail
#     s.sendmail(fromaddr, toaddr, text)
    
#     # terminating the session
#     s.quit()

# def send_contactUs_mailer(username:any, email:any, msg:any):
#     fromaddr = gmail_user
#     toaddr = email
#     subject = 'Thank you for contacting us'
#     body = render_template("contact_us.html", username=username, email=email, msg=msg)

#     msg = MIMEMultipart()
#     # storing the senders email address
#     msg['From'] = fromaddr
#     # storing the receivers email address 
#     msg['To'] = ", ".join(toaddr)
#     # storing the subject 
#     msg['Subject'] = subject
#     # string to store the body of the mail
#     body = body
#     # attach the body with the msg instance
#     msg.attach(MIMEText(body,'html', 'utf-8'))
    
#     # open the file to be sent 
#     filename = "keletick.png"
#     attachment = open("static/assets/logo.png", "rb")
    
#     # instance of MIMEBase and named as p
#     p = MIMEBase('application', 'octet-stream')
#     # To change the payload into encoded form
#     p.set_payload((attachment).read())
#     # encode into base64
#     encoders.encode_base64(p)
#     p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#     # attach the instance 'p' to instance 'msg'
#     msg.attach(p)
    
#     # creates SMTP session
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#     # s = smtplib.SMTP('smtppro.zoho.in', 587)

    
#     # start TLS for security
#     s.starttls()
    
#     # Authentication
#     s.login(fromaddr, gmail_password)
    
#     # Converts the Multipart msg into a string
#     text = msg.as_string()
    
#     # sending the mail
#     s.sendmail(fromaddr, toaddr, text)
    
#     # terminating the session
#     s.quit()