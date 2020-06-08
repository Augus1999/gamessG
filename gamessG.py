# -*- coding: utf-8 -*-
# Author Nianze A. TAO
import os
import sys
import subprocess as sp
from shutil import copyfile
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QInputDialog


class UiMainWindow(object):
    def __init__(self):
        self.cwd = os.getcwd()
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.textEdit = QtWidgets.QTextEdit(self.central_widget)
        self.pushButton1 = QtWidgets.QPushButton(self.central_widget)
        self.pushButton2 = QtWidgets.QPushButton(self.central_widget)
        self.pushButton3 = QtWidgets.QPushButton(self.central_widget)
        MainWindow.setWindowIcon(QtGui.QIcon('.\\ico\\base.png'))
        try:
            with open('gamessGd.gm', 'r', encoding='utf-8') as f:
                _dir = f.readlines()
            for _line in _dir:
                if 'GAMESSDIR' in _line:  # find gamess dir
                    self.gamess_dir = _line.strip('\n').split('=')[1]
                if 'OUTDIR' in _line:  # find output dir
                    self.out_dir = _line.strip('\n').split('=')[1]
            if not os.path.exists(self.out_dir):
                os.makedirs(self.out_dir)
        except FileNotFoundError:
            QMessageBox.warning(None, 'Error', 'Cannot find gamessGd.gm',
                                QMessageBox.Yes | QMessageBox.No)
            MainWindow.close()

    def setup_ui(self, main_window):
        main_window.setObjectName('MainWindow')
        main_window.resize(600, 100)
        main_window.setWindowOpacity(0.92)
        main_window.setStyleSheet('background-color: rgb(255, 255, 255);')
        main_window.setFixedSize(main_window.width(), main_window.height())
        main_window.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        # Taiwan is NOT a part of China!
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.6)
        self.pushButton1.setGeometry(QtCore.QRect(10, 20, 30, 30))
        self.pushButton2.setGeometry(QtCore.QRect(30, 60, 40, 30))
        self.pushButton3.setGeometry(QtCore.QRect(520, 25, 40, 40))
        self.textEdit.setGeometry(QtCore.QRect(70, 20, 500, 50))
        self.central_widget.setObjectName('central_widget')
        self.pushButton1.setObjectName('pushButton1')
        self.pushButton2.setObjectName('pushButton2')
        self.textEdit.setObjectName('textEdit')
        self.pushButton1.setToolTip('Add')
        self.pushButton2.setToolTip('open MacMolPlt')
        self.pushButton3.setToolTip('clean restart files')
        self.pushButton1.setStyleSheet('border-radius:20px;\n'
                                       'border-image: url(./ico/black-plus.png);')
        self.pushButton2.setStyleSheet('border-radius:20px;\n'
                                       'border-image: url(./ico/water_molecule.png);')
        self.pushButton3.setStyleSheet('border-radius:20px;\n'
                                       'border-image: url(./ico/clean_black.png);\n'
                                       'background-color: rgb(100, 100, 100);')
        self.textEdit.setStyleSheet('background-color: rgb(100, 100, 100);\n'
                                    'color: rgb(250, 250, 250);\n'
                                    'font: 20pt \"Adobe Arabic\";\n'
                                    'border-radius:20px;\n')
        self.pushButton1.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        self.pushButton2.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        self.pushButton3.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        self.pushButton3.setGraphicsEffect(op)
        self.textEdit.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        main_window.setCentralWidget(self.central_widget)
        self.re_translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def re_translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate('MainWindow', 'gamessG'))
        self.pushButton1.setWhatsThis(_translate('MainWindow', '<html><head/><body><p>Add</p></body></html>'))
        self.pushButton2.setWhatsThis(_translate('MainWindow', '<html><head/><body><p>Open</p></body></html>'))
        self.pushButton3.setWhatsThis(_translate('MainWindow', '<html><head/><body><p>Clean</p></body></html>'))
        self.pushButton1.clicked.connect(self._add)
        self.pushButton2.clicked.connect(self._open)
        self.pushButton3.clicked.connect(self._clean)

    def _add(self):
        # add project(s) to run.
        openfile_names, _ = QFileDialog.getOpenFileNames(None, '選擇文件', self.cwd, 'gamess input files(*.inp)')
        file_number = len(openfile_names)
        if file_number != 0:
            w = str()
            for item in openfile_names:
                w += (item+'\n')
            self.textEdit.setPlainText(w)
            n_cpu, __ = QInputDialog.getInt(None, 'processor', 'processors:', 4, 0, 16, 1)  # get number of CPUs
            if __ is True:  # if selection(s) confirmed
                for key, openfile_name in enumerate(openfile_names):
                    file = openfile_name.split(r'/')[-1]  # get input file name without father dir
                    _name = None  # this variable is for gamess version name
                    for root, dirs, files in os.walk(self.gamess_dir):
                        for name in files:
                            if name.endswith('.exe') and name.startswith('gamess.'):  # find gamess.*.exe
                                _name = name.strip('.exe').strip('gamess.')  # get version name
                                break
                    cmd = self.gamess_dir+'\\rungms.bat'+' '+file+' '+_name+' '+str(n_cpu)+' 0 >'\
                        + self.out_dir+'\\'+file.replace('.inp', '.log')  # command of rungms.bat
                    copyfile(openfile_name, self.gamess_dir+'\\'+file)  # copy input file to gamess dir
                    os.chdir(self.gamess_dir)  # cd to gamess dir
                    MainWindow.setWindowTitle('gamessG* pending')
                    ret_cod = sp.call(cmd, shell=True)  # run rungms.bat
                    if ret_cod == 0 and key == file_number-1:
                        MainWindow.setWindowTitle('gamessG  finished')
                    if ret_cod == 1:
                        MainWindow.setWindowTitle('gamessG  ERROR')
                    os.remove(self.gamess_dir+'\\'+file)
                else:
                    pass

    def _clean(self):
        # delete all restart files.
        text = 'Delete files: \n'
        name_ends = ['.dat', '.trj', '.efp', '.pot', '.rst', '.cosmo']  # file ends see ./restart/README.txt
        for root, _, files in os.walk(self.gamess_dir+'\\restart'):
            for name in files:
                for name_end in name_ends:
                    if name.endswith(name_end):
                        os.remove(os.path.join(root, name))  # remove restart files
                        text += os.path.join(root, name) + '\n'
        QMessageBox.information(None, 'clean', text,
                                QMessageBox.Yes | QMessageBox.No)

    def _open(self):
        # run wxMacMolPlt.exe
        os.chdir(self.cwd)
        ret_cod = sp.call('wxMacMolPlt.exe', shell=True)  # run wxMacMolPlt
        if ret_cod != 0:
            QMessageBox.warning(None, 'Error', 'Cannot find wxMacMolPlt.exe. \
                                               Please ensure it exists in Env Variables.',
                                QMessageBox.Yes | QMessageBox.No)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
