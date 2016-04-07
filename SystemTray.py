from PyQt4 import QtGui, QtCore
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
        self.media_player = parent.media_player
        self.timer = parent.timer
        self.start_info = parent.start_info
        self.stop_info = parent.stop_info
        self.hide_ui = parent.hide_ui
        self.show_ui = parent.show_ui
        self.central_widget = parent.central_widget
        self.hide_all = parent.hide_all

        self.setup_menu()

    def setup_menu(self):
        """
            Setup app indicator menu.
        :return: None
        """
        # menu

        self.show_action = QtGui.QAction("Show", self.tray_menu)
        self.connect(self.show_action, QtCore.SIGNAL("triggered()"), self.show_all)
        self.tray_menu.addAction(self.show_action)

        self.play_pause_action = QtGui.QAction("Play", self.tray_menu)
        self.connect(self.play_pause_action, QtCore.SIGNAL("triggered()"), self.play_pause)
        self.tray_menu.addAction(self.play_pause_action)

        quit_action = QtGui.QAction("Quit", self.tray_menu)
        self.connect(quit_action, QtCore.SIGNAL("triggered()"), self.quit_app)
        self.tray_menu.addAction(quit_action)

        # system tray icon

        self.tray_icon.setIcon(QtGui.QIcon(":/images/icon.png"))
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def show_all(self):
        print "show"
        self.show_ui()
        self.central_widget.show()

    def play_pause(self):
        """
            Play, pause radio stream.
        :return: None
        """
        if self.media_player.is_playing():
            print "pause"
            self.media_player.pause()
            self.play_pause_action.setText("Play")
            self.stop_info()
            self.hide_all()
        else:
            print "play"
            self.media_player.play()
            self.play_pause_action.setText("Pause")
            self.start_info()
            self.show_all()

    @staticmethod
    def quit_app():
        """
            Close application.
        :return: None
        """
        print "quit"
        sys.exit()
