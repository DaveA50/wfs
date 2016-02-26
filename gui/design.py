# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_disconnect = QtGui.QPushButton(self.groupBox)
        self.btn_disconnect.setEnabled(False)
        self.btn_disconnect.setObjectName(_fromUtf8("btn_disconnect"))
        self.gridLayout_2.addWidget(self.btn_disconnect, 0, 1, 1, 1)
        self.btn_connect = QtGui.QPushButton(self.groupBox)
        self.btn_connect.setObjectName(_fromUtf8("btn_connect"))
        self.gridLayout_2.addWidget(self.btn_connect, 0, 0, 1, 1)
        self.btn_debug = QtGui.QPushButton(self.groupBox)
        self.btn_debug.setObjectName(_fromUtf8("btn_debug"))
        self.gridLayout_2.addWidget(self.btn_debug, 1, 1, 1, 1)
        self.btn_settings = QtGui.QPushButton(self.groupBox)
        self.btn_settings.setObjectName(_fromUtf8("btn_settings"))
        self.gridLayout_2.addWidget(self.btn_settings, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 2, 1, 1)
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menu_quit = QtGui.QAction(MainWindow)
        self.menu_quit.setObjectName(_fromUtf8("menu_quit"))
        self.menu_save_measurement_data = QtGui.QAction(MainWindow)
        self.menu_save_measurement_data.setObjectName(_fromUtf8("menu_save_measurement_data"))
        self.menu_settings = QtGui.QAction(MainWindow)
        self.menu_settings.setObjectName(_fromUtf8("menu_settings"))
        self.menuFile.addAction(self.menu_settings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menu_save_measurement_data)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menu_quit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "WFS Application", None))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox", None))
        self.btn_disconnect.setText(_translate("MainWindow", "Disconnect", None))
        self.btn_connect.setText(_translate("MainWindow", "Connect", None))
        self.btn_debug.setText(_translate("MainWindow", "Debug", None))
        self.btn_settings.setText(_translate("MainWindow", "Settings", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menu_quit.setText(_translate("MainWindow", "Quit", None))
        self.menu_save_measurement_data.setText(_translate("MainWindow", "Save Measurement Data", None))
        self.menu_settings.setText(_translate("MainWindow", "Settings", None))

