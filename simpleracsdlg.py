#!/usr/bin/env python3
"""simpleracsdlg
"""

import sys
import bisect
import pickle
import gzip
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import userdata
import ui_simpleracsdlg

CODEC = "utf-8"

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
                "选择上传文件", path)
        if fname:
            self.__debug = fname
            self.updateUi()

    @pyqtSignature("")
    def on_uploadButton_clicked(self):
        self.add()
        self.datas.exportXml("./data.xml")

    @pyqtSignature("QString")
    def on_uaccountLineEdit_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_upasswordLineEdit_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QTableWidgetItem*")
    def on_table_itemClicked(self):
        data = self.currentData()
        self.accountLabel.setText(data.account)

    def updateTable(self, current=None):
    #    self.table.clear()
        self.table.setRowCount(len(self.datas))
    #    self.table.setColumnCount(2)
    #    self.table.setHorizontalHeaderLabels(["文件", "上传日期"])
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
        self.table.resizeColumnsToContents()
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
        account = self.uaccountLineEdit.text()
        acquired = QDate.currentDate()
        self.data = userdata.Data(account, "", self.__debug, acquired)
        self.datas.add(self.data)

    def updateUi(self):
        self.updateTable()
        self.udebugLabel.setText(self.__debug)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = SimpleracsDlg()
    form.show()
    app.exec_()
