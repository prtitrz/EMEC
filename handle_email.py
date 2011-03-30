#!/usr/bin/env python

import os
import smtplib
import mimetypes
import re
import getpass, poplib
import email
import imaplib
import random

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from PyQt4.QtCore import *

DEBUG = 1

class Worker(QThread):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self, account, filename, password, smtp_server, index):
        self.account = account
        self.filename = filename
        self.password = password
        self.smtp_server = smtp_server
        self.index = index
        self.start()

    def run(self):
        account = str(self.account)
        # Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['Subject'] = 'mask{0}mask_{1}'.format(self.index, str(self.filename))
        outer['To'] = account
        outer['From'] = account
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        fp = open(str(self.filename), 'rb')
        msg = MIMEBase(maintype, subtype)
    #    msg.set_payload(encodebytes(fp.read()).decode())
        msg.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(msg)
    #    msg.add_header('Content-Transfer-Encoding', 'base64')
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(str(self.filename)))
        outer.attach(msg)
        # Send the message
        composed = outer.as_string()
        if DEBUG:
            fp = open("./output", 'w')
            fp.write(composed)
            fp.close()
        else:
            s = smtplib.SMTP()
            s.set_debuglevel(DEBUG)
            s.connect(self.smtp_server)
            s.login(account, self.password)
            s.sendmail(account, account, composed)
            s.quit()




def send(account, filename, password, smtp_server, index):
    """generate a mime message
    Send the contents of a directory as a MIME message."""
    account = str(account)
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'mask{0}mask_{1}'.format(index, str(filename))
    outer['To'] = account
    outer['From'] = account
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)

    fp = open(str(filename), 'rb')
    msg = MIMEBase(maintype, subtype)
#    msg.set_payload(encodebytes(fp.read()).decode())
    msg.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(msg)
#    msg.add_header('Content-Transfer-Encoding', 'base64')
    msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(str(filename)))
    outer.attach(msg)
    # Send the message
    composed = outer.as_string()
    if DEBUG:
        FNAME = "./output" + str(random.randint(0, 100))
        #fp = open("./output", 'w')
        fp = open(FNAME, 'w')
        fp.write(composed)
        fp.close()
    else:
        s = smtplib.SMTP()
        s.set_debuglevel(DEBUG)
        s.connect(smtp_server)
        s.login(account, password)
        s.sendmail(account, account, composed)
        s.quit()


def receive_pop():

    temp = []

    M = poplib.POP3('pop.sina.com')
    M.user('forpythontest@sina.com')
    M.pass_(getpass.getpass())
    numMessages = len(M.list()[1])

    for i in range(numMessages):
        for j in M.retr(i+1)[1]:
            temp.append(j)

        body = "\n".join(temp)
        begin = re.search("Content", body)
        print (body[begin.start():])
        msg = email.message_from_string(body[begin.start():])
        counter = 1
        for part in msg.walk():
            # multipart/* are just containers
            if part.get_content_maintype() == 'multipart':
                continue
           # Applications should really sanitize the given filename so that
           # an email message can't be used to overwrite import files
            filename = part.get_filename()
            if not filename:
                ext = mimetypes.guess_extension(part.get_content_type())
                if not ext:
                    # Use a generic bag of bits extension
                    ext = '.bin'
                filename = 'part-%03d%s' % (counter, ext)
            counter += 1
            fp = open(os.path.join(".", filename), 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

def receive_imap(account, password, mask, imap_server):

    M = imaplib.IMAP4_SSL(imap_server)
#    password = bytes(password, "ASCII")
    M.login(account, password)
    M.select()
    typ, data = M.search(None, 'SUBJECT', mask)
    for num in data[0].split():
        typ, msg_data = M.fetch(num, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
            #    msg = email.message_from_string((response_part[1]).decode())
                msg = email.message_from_string(response_part[1])
                counter = 1
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    filename = part.get_filename()
                    counter += 1
                    fp = open(os.path.join(".", filename), 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close
    M.close()
    M.logout()
