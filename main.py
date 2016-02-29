"""
Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)
"""
import subprocess
import sys

from wfs import WFS

if 'pyside' in sys.argv[1]:
    from PySide import QtCore, QtGui
    Signal = QtCore.Signal
    Slot = QtCore.Slot
    subprocess.call("pyside-uic.exe gui/design.ui -o gui/design.py")
else:
    from PyQt4 import QtCore, QtGui
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
    subprocess.call("pyuic4.bat gui/design.ui -o gui/design.py")

import gui


class WFSApp(QtGui.QMainWindow, gui.design.Ui_main_window):
    def __init__(self, parent=None, wfs=WFS()):
        super(WFSApp, self).__init__(parent)
        self.setupUi(self)
        self.wfs = wfs

        self.action_quit.triggered.connect(self.on_quit_trigger)
        self.action_connect.triggered.connect(self.on_connect_click)
        self.action_disconnect.triggered.connect(self.on_disconnect_click)
        self.btn_settings.clicked.connect(lambda: self.on_settings_click('Debug'))
        self.action_settings.triggered.connect(lambda: self.on_settings_click('Debug'))
        self.btn_debug.clicked.connect(self.on_debug_click)

    @Slot()
    def on_quit_trigger(self):
        self.close()

    @Slot()
    def on_connect_click(self):
        self.wfs.connect()
        self.action_disconnect.setEnabled(True)
        self.action_connect.setEnabled(False)

    @Slot()
    def on_disconnect_click(self):
        if self.wfs._close() == 0:
            self.action_connect.setEnabled(True)
            self.action_disconnect.setEnabled(False)

    @Slot(str)
    def on_settings_click(self, arg1):
        print(arg1)

    @Slot()
    def on_debug_click(self):
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
