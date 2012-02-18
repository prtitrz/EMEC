#!/usr/bin/env python

import os
import re

global VERBOSE
VERBOSE=False

import zfec
import handle_email
import userdata

PREFIX = "test"
SUFFIX = ".fec"
MAILSUFFIX = ["@163.com", "@126.com", "@gmail.com"]
SMPT_SERVER = ["smtp.163.com", "smtp.126.com"]
IMAP_SERVER = ["imap.163.com", "imap.126.com"]

from PyQt4.QtCore import *


class Worker(QThread):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self, choose, data, index):
        #self.account = account
        #self.index = index
        self.choose = choose
        self.data = data
        self.filename = data.fname
        self.index = index
        self.start()

    def run(self):
        if self.choose == "upload":
            self.encode(3, 5, self.filename)
            RE = re.compile(zfec.filefec.RE_FORMAT % (PREFIX, SUFFIX,))
            fns = os.listdir(".")
            sharefs = [ os.path.join(".", fn) for fn in fns if RE.match(fn) ]
            for i in range(5):
                account = self.data.account[i]
                maintype, subtype = account.split('/', 1)
                account = maintype + MAILSUFFIX[int(subtype)]
                password = self.data.password[i]
                smtp = SMPT_SERVER[int(subtype)]
                handle_email.send(account, sharefs[i], password, smtp, self.index)
                os.remove(sharefs[i])
        elif self.choose == "download":
            for i in range(5):
                account = self.data.account[i]
                maintype, subtype = account.split('/', 1)
                account = maintype + MAILSUFFIX[int(subtype)]
                password = self.data.password[i]
                imap = IMAP_SERVER[int(subtype)]
                mask = 'mask' + str(self.index) + 'mask'
                handle_email.receive_imap(account, password, mask, imap)
            self.decode(self.filename)


    def encode(self, k, m ,TESTFNAME, numshs=None):
        if numshs ==None:
            numshs = m

        #TESTFNAME = self.filename
        fsize = os.path.getsize(TESTFNAME)
        tempf = open(TESTFNAME, 'r+b')

        # encode the file
        zfec.filefec.encode_to_files(tempf, fsize, ".", PREFIX, k, m, SUFFIX, verbose=VERBOSE)
        tempf.close()

    def decode(self, TESTFNAME):

        RE = re.compile(zfec.filefec.RE_FORMAT % (PREFIX, SUFFIX,))
        fns = os.listdir(".")
        sharefs = [ open(os.path.join(".", fn), 'rb') for fn in fns if RE.match(fn) ]
        outf = open(TESTFNAME, 'w+b')
        zfec.filefec.decode_from_files(outf, sharefs, verbose=VERBOSE)
        outf.flush()
        outf.seek(0)
        outf.close()
