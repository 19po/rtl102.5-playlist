from PyQt4 import QtGui, QtCore, QtWebKit
from SystemTray import SystemTray
import icon

__author__ = 'postrowski'

# -*-coding: utf-8-*-


class MainUI(QtGui.QMainWindow):
    """
        Class MainUI which setup widgets and events.
    """

    signalDoubleClick = QtCore.pyqtSignal()

    def __init__(self, parent=None):

        super(MainUI, self).__init__(parent)
        self.central_widget = QtGui.QWidget()
        self.timer_show = QtCore.QTimer()
        self.programWebView = QtWebKit.QWebView()
        self.coverWebView = QtWebKit.QWebView()
        self.programLabel = QtGui.QLabel()
        self.nowPlayingLabel = QtGui.QLabel()
        self.logoLabel = QtGui.QLabel()
        self.tray_menu = QtGui.QMenu()
        self.tray_icon = QtGui.QSystemTrayIcon()

        # hide message after double click on it
        self.connect(self, QtCore.SIGNAL("signalDoubleClick()"), self.hide)

        # System Tray Icon
        SystemTray(self)

        # setup UI
        self.setup_ui()

    def setup_ui(self):
        """
            Setup user interface (UI) widgets.
        :return: None
        """

        self.nowPlayingLabel.setStyleSheet("QLabel {color : white; background-color: None}")
        self.nowPlayingLabel.hide()

        self.programLabel.setStyleSheet("QLabel {color : white; background-color: None}")
        self.programLabel.hide()

        self.coverWebView.setFixedSize(120, 120)
        self.coverWebView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.coverWebView.setStyleSheet("QWebView {background-color: rgba(30, 30, 30, 90%)}")
        self.coverWebView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.coverWebView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        self.coverWebView.hide()

        self.programWebView.setFixedSize(70, 70)
        self.programWebView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.programWebView.setStyleSheet("QWebView {background-color: rgba(30, 30, 30, 90%)}")
        self.programWebView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.programWebView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        self.programWebView.hide()

        self.timer_show.start(100)  # timer_show initial state

        pixmap = QtGui.QPixmap(":/images/icon.png")
        self.logoLabel.setPixmap(pixmap)
        self.logoLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.logoLabel.setFixedSize(self.coverWebView.width(), self.coverWebView.height())
        self.logoLabel.hide()

        # layout

        self.central_widget.setStyleSheet(
            ".QWidget { background-color: rgba(30, 30, 30, 90%); border-style: solid; border-radius: 20px; border-width: 20 } \
            QWidget:hover { background-color: rgba(30, 30, 30, 70%) }")
        self.central_widget.setToolTip("Double click to hide")
        self.central_widget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.central_widget.hide()

        grid = QtGui.QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.coverWebView, 1, 1, 2, 1)
        grid.addWidget(self.logoLabel, 1, 1, 2, 2)
        grid.addWidget(self.nowPlayingLabel, 1, 2, 1, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.programWebView, 1, 3, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(self.programLabel, 2, 3, 1, 1, QtCore.Qt.AlignCenter)
        self.central_widget.setLayout(grid)
        grid.setAlignment(self, QtCore.Qt.AlignRight)
        grid.setContentsMargins(20, 20, 20, 20)

        self.setCentralWidget(self.central_widget)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.SplashScreen)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setGeometry(self.width() * 2, self.height() / 2 - 150, 500, 170)

    def mouseDoubleClickEvent(self, event):
        """
            Hide UI after double clicked on it.
        :param event: event
        :return: None
        """

        self.signalDoubleClick.emit()

    def hide_ui(self):
        """
            Hide UI.
        :return: None
        """

        self.hide()

    def show_ui(self):
        """
            Show UI.
        :return: None
        """

        self.show()
