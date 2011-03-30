#!/usr/bin/env python

"""simpleracsdlg
"""

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import userdata
import handle_email
import ui_simpleracsdlg
import fec

CODEC = "utf-8"
suffix = ["@163.com", "@126.com", "@gmail.com"]
smtp_server = ["smtp.163.com", "smtp.126.com"]
imap_server = ["imap.163.com"]

class SimpleracsDlg(QDialog,
        ui_simpleracsdlg.Ui_SimpleracsDlg):
    """docstring for SimpleracsDlg"""
    def __init__(self, parent = None):
        super(SimpleracsDlg, self).__init__(parent)
        #self.thread = handle_email.Worker()
        self.thread = fec.Worker()
        self.datas = userdata.DataContainer()
        self.datas.importSAX("./data.xml")
        self.__debug = ""
        #self.uploadButton.setEnabled(False)
        self.setupUi(self)
        self.updateUi()

    @pyqtSignature("")
    def on_selectButton_clicked(self):
        #path = (QFileInfo(self.filename)).path()
        path = "."
        fname = QFileDialog.getOpenFileName(self,
                "open file", path)
        if fname:
            self.__debug = fname
            self.udebugLabel.setText(self.__debug)

    @pyqtSignature("")
    def on_uploadButton_clicked(self):
        #self.thread.render(account, self.__debug, password, smtp, index)
        data = self.add()
        index = self.datas.index(data)
        self.thread.render("upload", data, index)
        self.datas.exportXml("./data.xml")
        self.updateUi()

    @pyqtSignature("")
    def on_downloadButton_clicked(self):
        data = self.currentData()
        index = self.datas.index(data)
        password = [self.anyObject(4, i).text() for i in range(5)]
        data.setpassword(password)
        #account = data.account
        #maintype, subtype = account.split('/', 1)
        #account = maintype + suffix[int(subtype)]
        #password = self.dpasswordLineEdit.text()
        #imap = imap_server[int(subtype)]
        #mask = 'mask' + str(self.datas.index(data)) + 'mask'
        #handle_email.receive_imap(account, password, mask, imap)
        self.thread.render("download", data, index)

    @pyqtSignature("QString")
    def on_uaccountLineEdit_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_uaccountLineEdit_2_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_uaccountLineEdit_3_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_uaccountLineEdit_4_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_uaccountLineEdit_5_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_upasswordLineEdit_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_upasswordLineEdit_2_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_upasswordLineEdit_3_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_upasswordLineEdit_4_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_upasswordLineEdit_5_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QTableWidgetItem*")
    def on_table_itemClicked(self):
        data = self.currentData()
        for i in range(5):
            account = data.account[i]
            maintype, subtype = account.split('/', 1)
            account = maintype + suffix[int(subtype)]
            #self.accountLabel.setText(account)
            self.anyObject(3, i).setText(account)

    def anyObject(self, which, who):
        self.__uacc = [self.uaccountLineEdit, self.uaccountLineEdit_2, \
                       self.uaccountLineEdit_3, self.uaccountLineEdit_4, \
                       self.uaccountLineEdit_5]
        self.__index = [self.comboBox, self.comboBox_2, self.comboBox_3, \
                        self.comboBox_4, self.comboBox_5]
        self.__upass = [self.upasswordLineEdit, self.upasswordLineEdit_2, \
                        self.upasswordLineEdit_3, self.upasswordLineEdit_4, \
                        self.upasswordLineEdit_5]
        self.__dacc = [self.accountLabel, self.accountLabel_2, \
                       self.accountLabel_3, self.accountLabel_4, \
                       self.accountLabel_5]
        self.__dpass = [self.dpasswordLineEdit, self.dpasswordLineEdit_2, \
                        self.dpasswordLineEdit_3, self.dpasswordLineEdit_4, \
                        self.dpasswordLineEdit_5]
        self.__choice = [self.__uacc, self.__index, self.__upass, \
                         self.__dacc, self.__dpass]
        return self.__choice[which][who]

    def check_enable(self):
        enable = not self.uaccountLineEdit.text().isEmpty() and not self.upasswordLineEdit.text().isEmpty() and \
                not self.uaccountLineEdit_2.text().isEmpty() and not self.upasswordLineEdit_2.text().isEmpty() and \
                not self.uaccountLineEdit_3.text().isEmpty() and not self.upasswordLineEdit_3.text().isEmpty() and \
                not self.uaccountLineEdit_4.text().isEmpty() and not self.upasswordLineEdit_4.text().isEmpty() and \
                not self.uaccountLineEdit_5.text().isEmpty() and not self.upasswordLineEdit_5.text().isEmpty() and \
                self.__debug is not ""
        return enable


    def updateTable(self, current=None):
        #self.table.clear()
        self.table.setRowCount(len(self.datas))
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        selected = None
        for row, data in enumerate(self.datas):
            item = QTableWidgetItem(data.fname)
            if current is not None and current == self.datas.index(data):
                selected = item
            item.__hash__ = self.datas.index(data)
            self.table.setItem(row, 0, item)
            item = QTableWidgetItem(data.acquired.toString(
                                    userdata.DATEFORMAT))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item)
        #self.table.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)

    def updateTable2(self, current=None):
        #self.table.clear()
        self.table_2.setRowCount(len(self.datas))
        #self.table_2.setAlternatingRowColors(True)
        selected = None
        for row, data in enumerate(self.datas):
            item = QTableWidgetItem(data.fname)
            if current is not None and current == self.datas.index(data):
                selected = item
            item.__hash__ = self.datas.index(data)
            self.table_2.setItem(row, 0, item)
            item = QTableWidgetItem(data.acquired.toString(
                                    userdata.DATEFORMAT))
            item.setTextAlignment(Qt.AlignCenter)
            self.table_2.setItem(row, 1, item)
        #self.table_2.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)


    def currentData(self):
        row = self.table.currentRow()
        if row > -1:
            item = self.table.item(row, 0)
            id = item.__hash__
            return self.datas.dataFromid(id)
        return None

    def add(self):
        account = [str(self.anyObject(0, i).text() + \
            "/" + str(self.anyObject(1, i).currentIndex())) for i in range(5)]
        password = [self.anyObject(2, i).text() for i in range(5)]
        #index = self.comboBox.currentIndex()
        #account = self.uaccountLineEdit.text() + "/" + str(index)
        acquired = QDate.currentDate()
        self.data = userdata.Data(account, password, self.__debug, acquired)
        self.datas.add(self.data)
        #return self.datas.index(self.data)
        return self.data

    def updateUi(self):
        self.updateTable()
        #self.updateTable2()
        self.udebugLabel.setText(self.__debug)
        enable = self.check_enable()
        self.uploadButton.setEnabled(enable)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = SimpleracsDlg()
    form.show()
    app.exec_()
