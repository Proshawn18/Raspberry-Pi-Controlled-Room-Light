#!/usr/bin/env python3

import os
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.0.26'  # IP Address of Raspberry Pi
host_port = 8000

import smtplib


def sendNoto():
    sender_email = "hawnscott171@gmail.com"

    rec_email = "cooljack3087@gmail.com"

    password="cmjwicntwahghhjy"
    message="It is ready"
    
    msg = message

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(sender_email, password)

    print("Login success")

    server.sendmail(sender_email, rec_email, msg)

    print("Email has been sent to ", rec_email)





def getTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return temp


class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {}</p>
           <form action="/" method="POST">
               Turn LED :
               <input type="submit" class="whom" name="submit" value="On">
               <input type="submit" class="whom" name="submit" value="Off">
           </form>
           </body>
           </html>
        '''
        temp = getTemperature()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]


        if post_data == 'On':
            #Send email
            print()
            sendNoto()
        else:
            #Send email
            print()
            sendNoto()

        print("LED is idk")
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()