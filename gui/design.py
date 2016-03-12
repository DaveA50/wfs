# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/design.ui'
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

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName(_fromUtf8("main_window"))
        main_window.resize(555, 541)
        self.centralwidget = QtGui.QWidget(main_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.group_box = QtGui.QGroupBox(self.centralwidget)
        self.group_box.setObjectName(_fromUtf8("group_box"))
        self.gridLayout_2 = QtGui.QGridLayout(self.group_box)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_debug = QtGui.QPushButton(self.group_box)
        self.btn_debug.setObjectName(_fromUtf8("btn_debug"))
        self.gridLayout_2.addWidget(self.btn_debug, 0, 2, 1, 1)
        self.btn_settings = QtGui.QPushButton(self.group_box)
        self.btn_settings.setObjectName(_fromUtf8("btn_settings"))
        self.gridLayout_2.addWidget(self.btn_settings, 0, 0, 1, 1)
        self.btn_test = QtGui.QPushButton(self.group_box)
        self.btn_test.setObjectName(_fromUtf8("btn_test"))
        self.gridLayout_2.addWidget(self.btn_test, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.group_box, 0, 2, 1, 1)
        self.text_browser = QtGui.QTextBrowser(self.centralwidget)
        self.text_browser.setObjectName(_fromUtf8("text_browser"))
        self.gridLayout.addWidget(self.text_browser, 1, 2, 1, 1)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 555, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_file = QtGui.QMenu(self.menubar)
        self.menu_file.setObjectName(_fromUtf8("menu_file"))
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        main_window.setStatusBar(self.statusbar)
        self.toolbar = QtGui.QToolBar(main_window)
        self.toolbar.setObjectName(_fromUtf8("toolbar"))
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.action_quit = QtGui.QAction(main_window)
        self.action_quit.setObjectName(_fromUtf8("action_quit"))
        self.action_save_measurement_data = QtGui.QAction(main_window)
        self.action_save_measurement_data.setObjectName(_fromUtf8("action_save_measurement_data"))
        self.action_settings = QtGui.QAction(main_window)
        self.action_settings.setObjectName(_fromUtf8("action_settings"))
        self.action_connect = QtGui.QAction(main_window)
        self.action_connect.setObjectName(_fromUtf8("action_connect"))
        self.action_disconnect = QtGui.QAction(main_window)
        self.action_disconnect.setEnabled(False)
        self.action_disconnect.setObjectName(_fromUtf8("action_disconnect"))
        self.menu_file.addAction(self.action_connect)
        self.menu_file.addAction(self.action_disconnect)
        self.menu_file.addAction(self.action_settings)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save_measurement_data)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)
        self.menubar.addAction(self.menu_file.menuAction())
        self.toolbar.addAction(self.action_connect)
        self.toolbar.addAction(self.action_disconnect)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(_translate("main_window", "WFS Application", None))
        self.group_box.setTitle(_translate("main_window", "Buttons", None))
        self.btn_debug.setText(_translate("main_window", "Debug", None))
        self.btn_settings.setText(_translate("main_window", "Settings", None))
        self.btn_test.setText(_translate("main_window", "Test", None))
        self.menu_file.setTitle(_translate("main_window", "File", None))
        self.toolbar.setWindowTitle(_translate("main_window", "toolBar", None))
        self.action_quit.setText(_translate("main_window", "&Quit", None))
        self.action_save_measurement_data.setText(_translate("main_window", "Save &Measurement Data", None))
        self.action_save_measurement_data.setShortcut(_translate("main_window", "Ctrl+S", None))
        self.action_settings.setText(_translate("main_window", "&Settings", None))
        self.action_settings.setShortcut(_translate("main_window", "Ctrl+Alt+S", None))
        self.action_connect.setText(_translate("main_window", "&Connect", None))
        self.action_connect.setShortcut(_translate("main_window", "F1", None))
        self.action_disconnect.setText(_translate("main_window", "&Disconnect", None))
        self.action_disconnect.setShortcut(_translate("main_window", "F2", None))

