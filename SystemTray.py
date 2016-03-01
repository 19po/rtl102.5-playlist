from PyQt4 import QtGui
import sys

__author__ = 'postrowski'

# -*-coding: utf-8-*-


class SystemTray(QtGui.QSystemTrayIcon):
    """
        Class System Tray which show app indicator and supports its actions.
    """

    def __init__(self, parent):
        super(SystemTray, self).__init__(parent)
        self.tray_menu = parent.tray_menu
        self.tray_icon = parent.tray_icon
        self.coverWebView = parent.coverWebView
        self.nowPlayingLabel = parent.nowPlayingLabel
        self.process_vlc = parent.process_vlc

        self.setup_menu()

    def setup_menu(self):
        """
            Setup app indicator menu.
        :return: None
        """

        # menu

        label = QtGui.QLabel()
        label.setPixmap(QtGui.QPixmap(self.coverWebView))
        text_label = QtGui.QLabel(self.nowPlayingLabel)

        w = QtGui.QWidget()
        grid = QtGui.QHBoxLayout()
        grid.addWidget(label)
        grid.addWidget(text_label)
        w.setLayout(grid)

        label_action = QtGui.QWidgetAction(self.tray_menu)
        label_action.setDefaultWidget(w)
        self.tray_menu.addAction(label_action)

        close_action = QtGui.QAction("Quit", self.tray_menu)
        close_action.triggered.connect(self.close_app)
        self.tray_menu.addAction(close_action)

        # system tray icon

        self.tray_icon.setIcon(QtGui.QIcon(":/images/icon.png"))
        self.tray_icon.setToolTip("RTL 102.5")
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def close_app(self):
        """
            Close cVLC and UI.
        :return: None
        """
        print "closed"
        self.process_vlc.close()
        sys.exit()
