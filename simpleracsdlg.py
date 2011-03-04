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

    def add(self):
        account = self.uaccountLineEdit.text()
        acquired = QDate.currentDate()
        self.data = userdata.Data(account, "", self.__debug, acquired)
        self.datas.add(self.data)

    def updateUi(self):
        self.udebugLabel.setText(self.__debug)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = SimpleracsDlg()
    form.show()
    app.exec_()
