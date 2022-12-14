# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\TAG\Code\wfs\gui\design.ui',
# licensing of 'C:\Users\TAG\Code\wfs\gui\design.ui' applies.
#
# Created: Wed Jul 11 18:28:03 2018
#      by: pyside2-uic  running on PySide2 5.11.1a1.dev1530708810518
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(618, 610)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.grid_central = QtWidgets.QGridLayout(self.central_widget)
        self.grid_central.setObjectName("grid_central")
        self.text_browser = QtWidgets.QTextBrowser(self.central_widget)
        self.text_browser.setObjectName("text_browser")
        self.grid_central.addWidget(self.text_browser, 0, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.toolbar = QtWidgets.QToolBar(main_window)
        self.toolbar.setObjectName("toolbar")
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.action_quit = QtWidgets.QAction(main_window)
        self.action_quit.setObjectName("action_quit")
        self.action_settings = QtWidgets.QAction(main_window)
        self.action_settings.setObjectName("action_settings")
        self.action_connect = QtWidgets.QAction(main_window)
        self.action_connect.setObjectName("action_connect")
        self.action_disconnect = QtWidgets.QAction(main_window)
        self.action_disconnect.setEnabled(False)
        self.action_disconnect.setObjectName("action_disconnect")
        self.action_stop = QtWidgets.QAction(main_window)
        self.action_stop.setEnabled(False)
        self.action_stop.setObjectName("action_stop")
        self.action_start = QtWidgets.QAction(main_window)
        self.action_start.setObjectName("action_start")
        self.action_debug = QtWidgets.QAction(main_window)
        self.action_debug.setObjectName("action_debug")
        self.action_test = QtWidgets.QAction(main_window)
        self.action_test.setObjectName("action_test")
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
        main_window.setWindowTitle(QtWidgets.QApplication.translate("main_window", "WFS Application", None, -1))
        self.menu_file.setTitle(QtWidgets.QApplication.translate("main_window", "File", None, -1))
        self.toolbar.setWindowTitle(QtWidgets.QApplication.translate("main_window", "toolBar", None, -1))
        self.action_quit.setText(QtWidgets.QApplication.translate("main_window", "&Quit", None, -1))
        self.action_settings.setText(QtWidgets.QApplication.translate("main_window", "&Settings", None, -1))
        self.action_settings.setShortcut(QtWidgets.QApplication.translate("main_window", "Ctrl+Alt+S", None, -1))
        self.action_connect.setText(QtWidgets.QApplication.translate("main_window", "&Connect", None, -1))
        self.action_connect.setToolTip(QtWidgets.QApplication.translate("main_window", "Connect to the WFS", None, -1))
        self.action_connect.setShortcut(QtWidgets.QApplication.translate("main_window", "F1", None, -1))
        self.action_disconnect.setText(QtWidgets.QApplication.translate("main_window", "&Disconnect", None, -1))
        self.action_disconnect.setToolTip(QtWidgets.QApplication.translate("main_window", "Disconnect from the WFS", None, -1))
        self.action_disconnect.setShortcut(QtWidgets.QApplication.translate("main_window", "F2", None, -1))
        self.action_stop.setText(QtWidgets.QApplication.translate("main_window", "Stop", None, -1))
        self.action_stop.setToolTip(QtWidgets.QApplication.translate("main_window", "Stop updating the WFS", None, -1))
        self.action_stop.setShortcut(QtWidgets.QApplication.translate("main_window", "Shift+F2", None, -1))
        self.action_start.setText(QtWidgets.QApplication.translate("main_window", "Start", None, -1))
        self.action_start.setToolTip(QtWidgets.QApplication.translate("main_window", "Start updating the WFS", None, -1))
        self.action_start.setShortcut(QtWidgets.QApplication.translate("main_window", "Shift+F1", None, -1))
        self.action_debug.setText(QtWidgets.QApplication.translate("main_window", "Debug", None, -1))
        self.action_debug.setToolTip(QtWidgets.QApplication.translate("main_window", "Debug command window", None, -1))
        self.action_test.setText(QtWidgets.QApplication.translate("main_window", "Test", None, -1))
        self.action_test.setToolTip(QtWidgets.QApplication.translate("main_window", "Test Function", None, -1))

