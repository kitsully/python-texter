""" 
This is a script designed to send text messages to phone numbers via email. It is a work in progress
Kristopher Sullivan 
January 2, 2013 
"""

import argparse
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

gmail_user = "" # Fill these in with the information matching the email account you will be using. 
gmail_pwd = ""


# Formulates the correct address to send the text to
def constructAddress(net, num):
    verizon = "@vtext.com"
    att = "@txt.att.net"
    tm = "@tmomail.net"
    address = ""
    if net.lower() == "a":
        address = att
    elif net.lower() == "v":
        address = verizon
    elif net.lower() == "t":
        address = tm
    else:
        print "You did not specify a valid network!!"
        sys.exit()
    address = num + address
    return address


def mail(to, subject, text):
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    fp = open(text, 'rb')

    msg.attach(MIMEText(fp.read()))

    mailServer = smtplib.SMTP("smtp.gmail.com", 587) # These are gmail's SMTP settings if you want to use another mail system you will need to set that up.
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()


def checkNumLen(num):
    if len(num) != 10:
        print "You did not specify a valid phone number!!"
        print "Number must be ten digits long."
        sys.exit()


def sendMessage(num, net, body, numTexts):
    checkNumLen(num)
    if numTexts == 0:
        mail(constructAddress(net, num), "", body)
    else:
        while numTexts > 0:
            mail(constructAddress(net, num), "", body)
            numTexts = numTexts - 1


def main():
    parser = argparse.ArgumentParser(description="Send a text.")
    parser.add_argument("network",
        help="Select the network you are sending to V (Verizon) or A (AT&T) T(T-mobile)")  # gets the network from command line
    parser.add_argument("number", help="Enter the ten digit number of the person you are sending to.")  # gets the number from command line
    parser.add_argument("--text", default="none",
        help="Enter relative path to the text file with the content of your message")
    parser.add_argument("--numTexts", default=0,
        type=int, help='Specifiy a multiple number of texts for "drive-by" texting')
    args = parser.parse_args()

    num = args.number
    net = args.network
    body = args.text
    numTexts = args.numTexts  # number of driveby texts to be sent

    sendMessage(num, net, body, numTexts)

main()
