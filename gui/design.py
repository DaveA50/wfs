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
        main_window.resize(618, 610)
        self.central_widget = QtGui.QWidget(main_window)
        self.central_widget.setObjectName(_fromUtf8("central_widget"))
        self.grid_central = QtGui.QGridLayout(self.central_widget)
        self.grid_central.setObjectName(_fromUtf8("grid_central"))
        self.text_browser = QtGui.QTextBrowser(self.central_widget)
        self.text_browser.setObjectName(_fromUtf8("text_browser"))
        self.grid_central.addWidget(self.text_browser, 0, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 21))
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
        self.action_settings = QtGui.QAction(main_window)
        self.action_settings.setObjectName(_fromUtf8("action_settings"))
        self.action_connect = QtGui.QAction(main_window)
        self.action_connect.setObjectName(_fromUtf8("action_connect"))
        self.action_disconnect = QtGui.QAction(main_window)
        self.action_disconnect.setEnabled(False)
        self.action_disconnect.setObjectName(_fromUtf8("action_disconnect"))
        self.action_stop = QtGui.QAction(main_window)
        self.action_stop.setEnabled(False)
        self.action_stop.setObjectName(_fromUtf8("action_stop"))
        self.action_start = QtGui.QAction(main_window)
        self.action_start.setObjectName(_fromUtf8("action_start"))
        self.action_debug = QtGui.QAction(main_window)
        self.action_debug.setObjectName(_fromUtf8("action_debug"))
        self.action_test = QtGui.QAction(main_window)
        self.action_test.setObjectName(_fromUtf8("action_test"))
        self.menu_file.addAction(self.action_connect)
        self.menu_file.addAction(self.action_disconnect)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_settings)
        self.menu_file.addAction(self.action_debug)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)
        self.menubar.addAction(self.menu_file.menuAction())
        self.toolbar.addAction(self.action_connect)
        self.toolbar.addAction(self.action_disconnect)
        self.toolbar.addAction(self.action_start)
        self.toolbar.addAction(self.action_stop)
        self.toolbar.addAction(self.action_test)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(_translate("main_window", "WFS Application", None))
        self.menu_file.setTitle(_translate("main_window", "File", None))
        self.toolbar.setWindowTitle(_translate("main_window", "toolBar", None))
        self.action_quit.setText(_translate("main_window", "&Quit", None))
        self.action_settings.setText(_translate("main_window", "&Settings", None))
        self.action_settings.setShortcut(_translate("main_window", "Ctrl+Alt+S", None))
        self.action_connect.setText(_translate("main_window", "&Connect", None))
        self.action_connect.setToolTip(_translate("main_window", "Connect to the WFS", None))
        self.action_connect.setShortcut(_translate("main_window", "F1", None))
        self.action_disconnect.setText(_translate("main_window", "&Disconnect", None))
        self.action_disconnect.setToolTip(_translate("main_window", "Disconnect from the WFS", None))
        self.action_disconnect.setShortcut(_translate("main_window", "F2", None))
        self.action_stop.setText(_translate("main_window", "Stop", None))
        self.action_stop.setToolTip(_translate("main_window", "Stop updating the WFS", None))
        self.action_stop.setShortcut(_translate("main_window", "Shift+F2", None))
        self.action_start.setText(_translate("main_window", "Start", None))
        self.action_start.setToolTip(_translate("main_window", "Start updating the WFS", None))
        self.action_start.setShortcut(_translate("main_window", "Shift+F1", None))
        self.action_debug.setText(_translate("main_window", "Debug", None))
        self.action_debug.setToolTip(_translate("main_window", "Debug command window", None))
        self.action_test.setText(_translate("main_window", "Test", None))
        self.action_test.setToolTip(_translate("main_window", "Test Function", None))

