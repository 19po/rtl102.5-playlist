from PyQt4 import QtGui, QtCore
import sys
from Playlist import Playlist
import vlc
import urllib

__author__ = 'postrowski'

# -*-coding: utf-8-*-


class SystemTray(QtGui.QSystemTrayIcon):
    """
        Class System Tray which show app indicator and supports its actions.
    """

    def __init__(self, parent):

        super(SystemTray, self).__init__(parent)
        self.sc = QtGui.QFileDialog()
        self.nowPlayingLabel = parent.nowPlayingLabel
        self.programLabel = parent.programLabel
        self.logoLabel = parent.logoLabel
        self.coverWebView = parent.coverWebView
        self.programWebView = parent.programWebView

        self.tray_menu = parent.tray_menu
        self.tray_icon = parent.tray_icon
        self.hide_ui = parent.hide_ui
        self.show_ui = parent.show_ui
        self.central_widget = parent.central_widget
        self.timer_show = parent.timer_show

        self.setup_menu()

        self.playlist = Playlist(self)

        self.instance = vlc.Instance()  # create a vlc instance
        self.player = self.instance.media_player_new()  # create a empty vlc media player
        stream = 'http://shoutcast.rtl.it:3010/stream/1/'
        option = '--extraintf=http'  # enable web interface
        self.media = self.instance.media_new(stream, option)  # create the media
        self.player.set_media(self.media)

        self.info_0 = None  # this variable always before set_meta_data call is None
        self.timer_check = QtCore.QTimer()
        self.connect(self.timer_check, QtCore.SIGNAL("timeout()"), self.set_meta_data)  # polling every second

        self.my_dict = {}

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

        self.stop_action = QtGui.QAction("Stop", self.tray_menu)
        self.connect(self.stop_action, QtCore.SIGNAL("triggered()"), self.stop)
        self.tray_menu.addAction(self.stop_action)
        self.stop_action.setVisible(False)

        self.save_cover_action = QtGui.QAction("Save album cover", self.tray_menu)
        self.connect(self.save_cover_action, QtCore.SIGNAL("triggered()"),
                     lambda: self.save_picture(self.my_dict["album_cover"],
                                               self.my_dict[u"artist_name"] + " - " + self.my_dict[u"album_title"]))
        self.tray_menu.addAction(self.save_cover_action)
        self.save_cover_action.setVisible(False)

        self.save_image_action = QtGui.QAction("Save program image", self.tray_menu)
        self.connect(self.save_image_action, QtCore.SIGNAL("triggered()"),
                     lambda: self.save_picture(self.my_dict["program_image"],
                                               self.my_dict[u"program_title"] + " - " + self.my_dict[u"speakers"]))
        self.tray_menu.addAction(self.save_image_action)
        self.save_image_action.setVisible(False)

        quit_action = QtGui.QAction("Quit", self.tray_menu)
        self.connect(quit_action, QtCore.SIGNAL("triggered()"), self.quit_app)
        self.tray_menu.addAction(quit_action)

        # system tray icon

        self.tray_icon.setIcon(QtGui.QIcon(":/images/icon.png"))
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def hide_all(self):
        """
            Hide UI.
        """

        self.hide_ui()
        self.central_widget.hide()

    def show_all(self):
        """"
            Show UI for 10 seconds, then hide it.
        """

        print "show"
        self.show_ui()
        self.central_widget.show()
        self.timer_show.start(10000)  # 10 seconds, display UI time in ms
        self.timer_show.timeout.connect(self.hide_all)

    def set_meta_data(self):
        """
            Set xml meta data and show message. Check if images are available to download.
        :return: None
        """

        info_1 = self.media.get_meta(vlc.Meta.NowPlaying)  # get xml data
        if info_1 != self.info_0:
            self.info_0 = info_1
            # print "now playing: {0}".format(self.info_0)
            self.playlist.set_info(self.playlist.xml_to_dict(self.info_0))
            self.playlist.show_msg()
            self.my_dict = self.playlist.xml_to_dict(self.info_0)
            # print "my_dict: ", self.my_dict

        if self.player.is_playing():

            try:
                if self.my_dict["album_cover"]:
                    self.save_cover_action.setVisible(True)
                else:
                    self.save_cover_action.setVisible(False)
            except TypeError:  # parse data delay when play button pressed
                pass

            try:
                if self.my_dict["program_image"]:
                    self.save_image_action.setVisible(True)
                else:
                    self.save_image_action.setVisible(False)
            except TypeError:  # parse data delay when play button pressed
                pass

    def play_pause(self):
        """
            Play or pause radio stream.
        :return: None
        """

        if self.player.is_playing():
            # print "paused"
            self.timer_show.killTimer(10)
            self.timer_check.stop()
            self.play_pause_action.setText("Paused")
            self.player.pause()
            self.hide_all()
            self.stop_action.setVisible(True)
        else:
            # print "play"
            self.timer_check.start(1000)
            self.play_pause_action.setText("Pause")
            self.player.play()
            self.set_meta_data()
            self.playlist.show_msg()
            self.stop_action.setVisible(True)

    def stop(self):
        """
            Stop stream.
        :return: None
        """

        # print "stop"
        self.player.stop()
        self.play_pause_action.setText("Play")
        self.stop_action.setVisible(False)
        self.save_cover_action.setVisible(False)
        self.save_image_action.setVisible(False)
        self.hide_all()

    @staticmethod
    def save_picture(url, file_name):
        """
            Save album cover and/or program image.
        :param url: file url
        :param file_name: file name
        :return: None
        """

        location = QtGui.QFileDialog()
        dir_path = QtCore.QDir()
        path = dir_path.homePath() + dir_path.separator() + unicode(file_name)
        file_path = location.getSaveFileName(location, "Save file as", path)

        if location:
            urllib.urlretrieve(url, unicode(file_path))

    @staticmethod
    def quit_app():
        """
            Close application.
        :return: None
        """

        # print "quit"
        sys.exit()
