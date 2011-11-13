import smtplib  

def send_message(toaddrs = 'peterqian1993@hotmail.com', msg = 'nothing'):

    fromaddr = 'ninjahelperberkeley@gmail.com'     
    # Credentials (if needed)  
    username = 'ninjahelperberkeley@gmail.com'  
    password = 'hack123456'  

    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, toaddrs, msg)  
    server.quit()  

# debug
send_message()
