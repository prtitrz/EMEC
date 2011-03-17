#!/usr/bin/env python

"""simpleracsdlg
"""

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import userdata
import handle_email
import ui_simpleracsdlg

CODEC = "utf-8"
suffix = ["@163.com", "@126.com", "@gmail.com"]
smtp_server = ["smtp.163.com"]
imap_server = ["imap.163.com"]

class SimpleracsDlg(QDialog,
        ui_simpleracsdlg.Ui_SimpleracsDlg):
    """docstring for SimpleracsDlg"""
    def __init__(self, parent = None):
        super(SimpleracsDlg, self).__init__(parent)
        self.datas = userdata.DataContainer()
        self.datas.importSAX("./data.xml")
        self.__debug = "test"
        self.setupUi(self)
        self.updateUi()

    @pyqtSignature("")
    def on_selectButton_clicked(self):
    #    path = (QFileInfo(self.filename)).path()
        path = "."
        fname = QFileDialog.getOpenFileName(self,
                "open file", path)
        if fname:
            self.__debug = fname
    #        self.updateUi()
            self.udebugLabel.setText(self.__debug)

    @pyqtSignature("")
    def on_uploadButton_clicked(self):
        temp = self.add()
        index = self.comboBox.currentIndex()
        account = self.uaccountLineEdit.text() + suffix[index]
        password = self.upasswordLineEdit.text()
        smtp = smtp_server[index]
        index = temp
        handle_email.send(account, self.__debug, password, smtp, index)
        self.datas.exportXml("./data.xml")
        self.updateUi()

    @pyqtSignature("")
    def on_downloadButton_clicked(self):
        data = self.currentData()
        account = data.account
        maintype, subtype = account.split('/', 1)
        account = maintype + suffix[int(subtype)]
        password = self.dpasswordLineEdit.text()
        imap = imap_server[int(subtype)]
        mask = str(self.datas.index(data)) + 'mask'
        handle_email.receive_imap(account, password, mask, imap)

    #@pyqtSignature("QString")
    #def on_uaccountLineEdit_textEdited(self, text):
    #    self.updateUi()

    #@pyqtSignature("QString")
    #def on_upasswordLineEdit_textEdited(self, text):
    #    self.updateUi()

    @pyqtSignature("QTableWidgetItem*")
    def on_table_itemClicked(self):
        data = self.currentData()
        account = data.account
        maintype, subtype = account.split('/', 1)
        account = maintype + suffix[int(subtype)]
        self.accountLabel.setText(account)

    def updateTable(self, current=None):
    #    self.table.clear()
        self.table.setRowCount(len(self.datas))
    #    self.table.setColumnCount(2)
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
    #    self.table.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)

    def updateTable2(self, current=None):
    #    self.table.clear()
        self.table_2.setRowCount(len(self.datas))
    #    self.table.setColumnCount(2)
    #    self.table_2.setAlternatingRowColors(True)
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
    #    self.table_2.resizeColumnsToContents()
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
        #account = self.uaccountLineEdit.text()
        index = self.comboBox.currentIndex()
        account = self.uaccountLineEdit.text() + "/" + str(index)
        acquired = QDate.currentDate()
        self.data = userdata.Data(account, "", self.__debug, acquired)
        self.datas.add(self.data)
        return self.datas.index(self.data)

    def updateUi(self):
        self.updateTable()
        self.updateTable2()
        self.udebugLabel.setText(self.__debug)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = SimpleracsDlg()
    form.show()
    app.exec_()
