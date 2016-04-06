from PyQt4 import QtGui, QtCore
import sys
# from time import sleep

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

        self.setup_menu()

    def setup_menu(self):
        """
            Setup app indicator menu.
        :return: None
        """
        # menu

        self.msg_action = QtGui.QAction("Show", self.tray_menu)
        self.connect(self.msg_action, QtCore.SIGNAL("triggered()"), self.msg)
        self.tray_menu.addAction(self.msg_action)

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

    def msg(self):
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
            self.hide_ui()
            self.central_widget.hide()
        else:
            print "play"
            self.media_player.play()
            self.play_pause_action.setText("Pause")
            # sleep(5)
            self.start_info()
            self.show_ui()
            self.central_widget.show()

    @staticmethod
    def quit_app():
        """
            Close application.
        :return: None
        """
        print "quit"
        sys.exit()
