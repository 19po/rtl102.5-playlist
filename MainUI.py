from PyQt4 import QtGui, QtCore, QtWebKit
from Playlist import Playlist

__author__ = 'postrowski'

# -*-coding: utf-8-*-


class MainUI(QtGui.QMainWindow, Playlist):
    signalDoubleClick = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.timer = QtCore.QTimer()
        self.singleTimer = QtCore.QTimer()
        self.programWebView = QtWebKit.QWebView()
        self.coverWebView = QtWebKit.QWebView()
        self.programLabel = QtGui.QLabel()
        self.nowPlayingLabel = QtGui.QLabel()

        self.setup_ui()

        # self.timer.timeout.connect(self.json_change)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.json_change)

        # hide message indicator after double click on it
        self.signalDoubleClick.connect(self.hide)

    def setup_ui(self):
        self.nowPlayingLabel.setStyleSheet("QLabel {color : white; background-color: None}")

        self.programLabel.setStyleSheet("QLabel {color : white; background-color: None}")

        self.coverWebView.setFixedSize(120, 120)
        self.coverWebView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.coverWebView.setStyleSheet(
            "QWebView {background-color: rgba(30, 30, 30, 90%); border-style: solid; border-radius: 5px;}")
        self.coverWebView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.coverWebView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)

        self.programWebView.setFixedSize(70, 70)
        self.programWebView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.programWebView.setStyleSheet(
            "QWebView {background-color: rgba(30, 30, 30, 90%); border-style: solid; border-radius: 5px;}")
        self.programWebView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.programWebView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)

        self.timer.start(30)  # timer initial state

        # layout

        self.central_widget = QtGui.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            ".QWidget { background-color: rgba(30, 30, 30, 90%); border-style: solid; border-radius: 12px} \
            QWidget:hover { background-color: rgba(70, 70, 70, 90%)}")
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.SplashScreen)

        grid = QtGui.QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.coverWebView, 1, 1, 2, 1)
        grid.addWidget(self.nowPlayingLabel, 1, 2, 1, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.programWebView, 1, 3, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(self.programLabel, 2, 3, 1, 1, QtCore.Qt.AlignCenter)
        self.central_widget.setLayout(grid)
        grid.setAlignment(self, QtCore.Qt.AlignRight)
        self.setToolTip("Double click to hide")
        self.central_widget.hide()

        # geometry

        self.setGeometry(self.width() * 2, self.height() / 2 - 150, 400, 150)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

    def mouseDoubleClickEvent(self, event):
        self.signalDoubleClick.emit()

    def hide_ui(self):
        self.hide()

    def show_ui(self):
        self.show()
