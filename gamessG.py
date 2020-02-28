# -*- coding: utf-8 -*-
# Author Nianze A. TAO
import os
import sys
import subprocess as sp
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from shutil import copyfile
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox


class UiMainWindow(object):
    def __init__(self):
        self.cwd = os.getcwd()
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.textEdit = QtWidgets.QTextEdit(self.central_widget)
        self.pushButton1 = QtWidgets.QPushButton(self.central_widget)
        self.pushButton2 = QtWidgets.QPushButton(self.central_widget)
        MainWindow.setWindowIcon(QtGui.QIcon('.\\ico\\base.png'))
        with open('gamessGd.csv', 'r', encoding='utf-8') as f:
            _dir = f.read()
        self.gamess_dir = _dir.split('\n')[0]
        self.out_dir = _dir.split('\n')[1]
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(600, 100)
        main_window.setWindowOpacity(0.85)
        main_window.setStyleSheet("background-color: rgb(255, 255, 255);")
        main_window.setFixedSize(main_window.width(), main_window.height())
        main_window.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        self.pushButton1.setGeometry(QtCore.QRect(10, 20, 30, 30))
        self.pushButton2.setGeometry(QtCore.QRect(30, 60, 40, 30))
        self.textEdit.setGeometry(QtCore.QRect(70, 20, 500, 50))
        self.central_widget.setObjectName("central_widget")
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton2.setObjectName("pushButton2")
        self.textEdit.setObjectName("textEdit")
        self.pushButton1.setToolTip('Add')
        self.pushButton2.setToolTip('open MacMolPlt')
        self.pushButton1.setStyleSheet('border-radius:20px;\n'
                                       'border-image: url(./ico/blue-plus.png);')
        self.pushButton2.setStyleSheet('border-radius:20px;\n'
                                       'border-image: url(./ico/water_molecule.png);')
        self.textEdit.setStyleSheet("background-color: rgb(100, 100, 100);\n"
                                    "color: rgb(250, 250, 250);\n"
                                    "font: 20pt \"Adobe Arabic\";\n"
                                    "border-radius:20px;\n")
        self.pushButton1.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        self.textEdit.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        main_window.setCentralWidget(self.central_widget)
        self.re_translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def re_translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "gamessG"))
        self.pushButton1.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Add</p></body></html>"))
        self.pushButton2.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Open</p></body></html>"))
        self.textEdit.setHtml(_translate("MainWindow", ''))
        self.pushButton1.clicked.connect(self.add)
        self.pushButton2.clicked.connect(self._open)

    def add(self):
        openfile_name, _ = QFileDialog.getOpenFileName(None, '選擇文件', self.cwd, 'gamess input files(*.inp)')
        if openfile_name != '':
            self.textEdit.setPlainText(openfile_name)
            file = openfile_name.split(r'/')[-1]
            _name = None
            for root, dirs, files in os.walk(self.gamess_dir):
                for name in files:
                    if name.endswith('.exe') and name.startswith('gamess.'):
                        _name = name.strip('.exe').strip('gamess.')
                        break
            cmd = self.gamess_dir+'\\rungms.bat'+' '+file+' '+_name+' 4 0 >'\
                + self.out_dir+'\\'+file.replace('.inp', '.log')
            copyfile(openfile_name, self.gamess_dir+'\\'+file)
            os.chdir(self.gamess_dir)
            sleep(1.0)
            p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
            while True:
                line = p.stdout.readline()
                MainWindow.setWindowTitle('gamessG* pending')
                if not line:
                    MainWindow.setWindowTitle('gamessG  finished')
                    break
            os.remove(self.gamess_dir+'\\'+file)

    def _open(self):
        os.chdir(self.cwd)
        ret_cod = sp.call('wxMacMolPlt.exe', shell=True)
        if ret_cod != 0:
            QMessageBox.warning(None, "Error", "Cannot find wxMacMolPlt.exe. \
                                               Please ensure it exists in Env Variables.",
                                QMessageBox.Yes | QMessageBox.No)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
