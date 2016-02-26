"""
Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)
"""
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject, SIGNAL

import gui
from wfs import WFS


class WFSApp(QtGui.QMainWindow, gui.design.Ui_MainWindow):
    def __init__(self, parent=None, wfs=WFS()):
        super(WFSApp, self).__init__(parent)
        self.setupUi(self)
        self.wfs = wfs
        QObject.connect(self.btn_connect, SIGNAL('clicked()'),
                        self.on_connect_click)
        QObject.connect(self.btn_disconnect, SIGNAL('clicked()'),
                        self.on_disconnect_click)
        QObject.connect(self.btn_settings, SIGNAL('clicked()'),
                        self.on_settings_click)
        QObject.connect(self.btn_debug, SIGNAL('clicked()'),
                        lambda: self.on_debug_click('Open settings window'))
        QObject.connect(self.menu_settings, SIGNAL('triggered()'),
                        self.on_settings_click)

    @QtCore.pyqtSlot()
    def on_connect_click(self):
        self.wfs.connect()
        self.btn_disconnect.setEnabled(True)
        self.btn_connect.setEnabled(False)

    @QtCore.pyqtSlot()
    def on_disconnect_click(self):
        if self.wfs._close() == 0:
            self.btn_connect.setEnabled(True)
            self.btn_disconnect.setEnabled(False)

    @QtCore.pyqtSlot()
    def on_settings_click(self):
        print('TODO')

    @QtCore.pyqtSlot(str)
    def on_debug_click(self, arg1):
        def loop_images(n):
            for i in xrange(n):
                self.wfs._take_spotfield_image_auto_exposure()
                self.wfs._get_spotfield_image()
                self.wfs._calc_spots_centroid_diameter_intensity()
                self.wfs._get_spot_centroids()
                self.wfs._calc_beam_centroid_diameter()
                self.wfs._calc_spot_to_reference_deviations()
                self.wfs._get_spot_deviations()
                self.wfs._calc_wavefront()
                self.wfs._calc_wavefront_statistics()
                self.wfs._zernike_lsf()

        print(arg1)
        self.wfs.connect()
        self.wfs._set_reference_plane(0)
        self.wfs._get_reference_plane()
        self.wfs._set_pupil()
        self.wfs._get_pupil()
        self.wfs._get_status()
        self.wfs._take_spotfield_image_auto_exposure()
        self.wfs._get_status()
        self.wfs._take_spotfield_image_auto_exposure()
        self.wfs._get_status()
        self.wfs._take_spotfield_image_auto_exposure()
        self.wfs._get_status()
        self.wfs._take_spotfield_image_auto_exposure()
        self.wfs._error_message(wfs._get_status())
        self.wfs._error_message(wfs._take_spotfield_image_auto_exposure())
        self.wfs._create_default_user_reference()
        self.wfs._save_user_reference_file()
        self.wfs._load_user_reference_file()
        self.wfs._error_message(wfs._do_spherical_reference())
        self.wfs._set_calc_spots_to_user_reference()
        self.wfs._set_spots_to_user_reference()
        loop_images(0)


def main(wfs):
    app = QtGui.QApplication(sys.argv)
    form = WFSApp(wfs=wfs)
    form.show()
    app.exec_()

if __name__ == '__main__':
    wfs = WFS()
    main(wfs)
