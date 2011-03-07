#!/usr/bin/env python3
"""userdata handler
"""

from PyQt4.QtCore import *
from PyQt4.QtXml import *

CODEC = "utf-8"
DATEFORMAT = "ddd MMM d, yyyy"

class Data(object):
    """docstring for Data"""
    def __init__(self, account=None, password="", fname=None, acquired=None):
        self.account = account
        self.password = password
        self.fname = fname
    #    self.acquired = QDate.currentDate()
        self.acquired = acquired


class DataContainer(object):
    """docstring for DataContainer"""
    def __init__(self):
        self.__datas = []

    def clear(self):
        self.__datas = []

    def dataFromid(self, id):
        """Returns the data with the given Python ID."""
        return self.__datas[id]

    def add(self, data):
    #    self.__datas[id(data)] = data
    #    self.num = len(self.__datas)
    #    self.__datas[self.num] = data
        self.__datas.append(data)

    def index(self, data):
        return self.__datas.index(data)

    def __iter__(self):
    #    for pair in iter(self.__datas):
    #        yield self.__datas[pair]
        for pair in range(len(self.__datas)):
            yield self.__datas[pair]

    def __len__(self):
        return len(self.__datas)


    #Xml writer
    def exportXml(self, fname):
        error = None
        fh = None
        try:
            fh = QFile(fname)
            #if QFile.exists(fname):
            #    if not fh.open(QIODevice.Append):
            #        raise IOError(fh.errorString())
            #    stream = QTextStream(fh)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec(CODEC)
            stream << ("<?xml version='1.0' encoding='{}'?>\n"
                   "<!DOCTYPE DATAS>\n".format(CODEC))
            stream << "<DATAS VERSION='1.0'>\n"

            for id in self.__datas:
                data = self.__datas[id]
                stream << ("<DATA LOCATION='{}' ACQUIRED='{}'>\n"
                           .format(data.fname,
                                   data.acquired.toString(Qt.ISODate))) \
                       << "<ACCOUNT>" <<Qt.escape(data.account) \
                       << "</ACCOUNT>\n</DATA>\n"
            stream << "</DATAS>\n"
        except EnvironmentError as e:
            error = "Failed to export: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error

    #Xml reader
    def importSAX(self, fname = "./data.xml"):
        error = None
        fh = None
        try:
            handler = SaxHandler(self)
            parser = QXmlSimpleReader()
            parser.setContentHandler(handler)
            parser.setErrorHandler(handler)
            fh = QFile(fname)
            input = QXmlInputSource(fh)
            self.clear()
            if not parser.parse(input):
                raise ValueError(handler.error)
        except (IOError, OSError, ValueError) as e:
            error = "Failed to import: {}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
        #    self.__fname = ""


class SaxHandler(QXmlDefaultHandler):

    def __init__(self, datas):
        super(SaxHandler, self).__init__()
        self.datas = datas
        self.text = ""
        self.error = None


    def clear(self):
        self.account = None
        self.fname = None
        self.acquired = None


    def startElement(self, namespaceURI, localName, qName, attributes):
        if qName == "DATA":
            self.clear()
            self.fname = attributes.value("LOCATION")
            ymd = attributes.value("ACQUIRED").split("-")
            if len(ymd) != 3:
                raise ValueError("invalid acquired date {}".format(
                        attributes.value("ACQUIRED")))
            self.acquired = QDate(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        elif qName in ("ACCOUNT", ):
            self.text = ""
        return True


    def characters(self, text):
        self.text += text
        return True


    def endElement(self, namespaceURI, localName, qName):
        if qName == "DATA":
    #        if (self.year is None or self.minutes is None or
    #            self.acquired is None or self.title is None or
    #            self.notes is None):
    #            raise ValueError("incomplete movie record")
            self.datas.add(Data(self.account, "", self.fname, self.acquired))
            self.clear()
        elif qName == "ACCOUNT":
            self.account = self.text.strip()
    #    elif qName == "NOTES":
    #        self.notes = self.text.strip()
        return True


    def fatalError(self, exception):
        self.error = "parse error at line {} column {}: {}".format(
                exception.lineNumber(), exception.columnNumber(),
                exception.message())
        return False


