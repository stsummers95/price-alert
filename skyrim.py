import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from bs4 import BeautifulSoup
import requests

import os
from dotenv import load_dotenv

load_dotenv()

url = "https://store.steampowered.com/app/489830/The_Elder_Scrolls_V_Skyrim_Special_Edition/"

def send_email(price, is_error):
    #print("Sending email...")
    port = 465
    smtp_server = "smtp.gmail.com"
    password = os.environ.get('EMAIL_PASSWORD')
    sender_email = os.environ.get('EMAIL_NAME')
    recipients = ["stephen.summers95@yahoo.com", "ssumm95@icloud.com"]
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    text = ""
    html = ""
    if is_error:
        #print("Preparing error message")
        message["Subject"] = "Error in finding price"
        text = """\
        Subject: Error in finding price
        
        There was an error finding the price of your item. Here is the error message:\n\n""" + price + """\n\nVisit the site: """ + url
        html = """\
        <html>
            <body>
                <p>There was an error in finding the price of your item. Here is the error message:<br><br>""" + price + """<br><br>Visit the site: <a href=\"""" + url + """\">""" + url + """</a></p>
            </body>
        </html>"""
    else:
        #print("Preparing success message")
        message["Subject"] = "Lowered price"
        text = """\
        Subject: Lowered price

        The price of your item was lowered! Here is the new price: """ + price
        html = """\
        <html>
            <body>
                <p>The price of your item was lowered! Here is the new price:<br><br>""" + price + """<br><br>Visit the site: <a href=\"""" + url + """\">""" + url + """</a></p>
            </body>
        </html>"""
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create a secure SSL context
    context_var = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp_server, port, context=context_var) as server:
        server.login("jarvisAutoSense@gmail.com", password)
        server.sendmail(sender_email, recipients, message.as_string())
        #print("Done!")

#print("Starting...")
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, "html.parser")
price = ""

try:
    price = soup.find(class_="game_purchase_price").get_text().strip()
    #if price doesn't match original price
    send_email(price, False)
except Exception as e:
    send_email(str(e), True)

