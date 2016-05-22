from PyQt4 import QtCore
from xml.dom.minidom import parseString
import re
from xml.parsers.expat import ExpatError

__author__ = 'postrowski'

# -*-coding: utf-8-*-


class Playlist(object):
    """
        Class Playlist which get information and show it.
    """

    def __init__(self, parent):

        self.nowPlayingLabel = parent.nowPlayingLabel
        self.programLabel = parent.programLabel
        self.logoLabel = parent.logoLabel
        self.coverWebView = parent.coverWebView
        self.programWebView = parent.programWebView
        self.timer_show = parent.timer_show
        self.central_widget = parent.central_widget
        self.hide_ui = parent.hide_ui
        self.show_ui = parent.show_ui

    @staticmethod
    def xml_to_dict(xml_data):
        """
            Get information from xml data and return dictionary.
        :param xml_data: xml data
        :return: dictionary
        """

        try:
            dom = parseString(xml_data)
            node = dom.childNodes
        except (ExpatError, TypeError):
            return False

        info_dict = {"program_title": "", "speakers": "", "program_image": "",
                     "song_title": "", "album_title": "", "artist_name": "", "album_cover": ""}

        try:
            info_dict["program_title"] = uni(node[0].getElementsByTagName("prg_title")[0].firstChild.data)
            info_dict["speakers"] = uni(node[0].getElementsByTagName("speakers")[0].firstChild.data)
            info_dict["program_image"] = node[0].getElementsByTagName("image170")[0].firstChild.data

            info_dict["song_title"] = uni(node[0].getElementsByTagName("mus_sng_title")[0].firstChild.data)
            info_dict["artist_name"] = uni(node[0].getElementsByTagName("mus_art_name")[0].firstChild.data)
            info_dict["album_title"] = uni(node[0].getElementsByTagName("mus_sng_itunesalbumname")[0].firstChild.data)
            info_dict["album_cover"] = node[0].getElementsByTagName("mus_sng_itunescoverbig")[0].firstChild.data
        except (IndexError, AttributeError):
            pass
        # print "info dict: ", info_dict
        return info_dict

    def set_info(self, info_dict):
        """
            Set information in UI.
        :param info_dict:
        :return: None
        """

        song_cover, artist_song, program_speakers, program_image = '', '', '', ''

        try:
            song_cover = info_dict["album_cover"]
            artist_song = info_dict["artist_name"] + '\n' + info_dict["song_title"]
            program_speakers = info_dict["program_title"] + '\n' + info_dict["speakers"]
            program_image = info_dict["program_image"]
        except TypeError:
            pass

        # display data
        if song_cover:
            self.logoLabel.hide()
            self.coverWebView.show()
            self.coverWebView.load(QtCore.QUrl(song_cover))
        else:
            self.coverWebView.hide()
            self.logoLabel.show()

        if artist_song:
            self.nowPlayingLabel.show()
            self.nowPlayingLabel.setText(artist_song)
        else:
            self.nowPlayingLabel.hide()

        if program_speakers:
            self.programLabel.show()
            self.programLabel.setText(program_speakers)
        else:
            self.programLabel.hide()

        if program_image:
            self.programWebView.show()
            self.programWebView.load(QtCore.QUrl(program_image))
        else:
            self.programWebView.hide()

            # for k, v in info_dict.items():
            #     print("{:15}{:2}{:1}".format(k, ":", v.encode('utf-8')))

    def hide_all(self):
        """
            Hide UI.
        :return:
        """

        self.hide_ui()
        self.central_widget.hide()

    def show_msg(self):
        """
            Resize central widget. Show UI for 10 seconds, then hide it.
        :return: None
        """

        self.show_ui()
        self.central_widget.show()

        # resize central widget; not smaller than fixed size
        size = self.central_widget.size()
        new_size = self.central_widget.sizeHint()
        if size < self.central_widget.resize(new_size):
            self.central_widget.resize(new_size)
        elif size > self.central_widget.resize(new_size):
            self.central_widget.resize(size)

        self.timer_show.start(10000)  # 10 seconds, display UI time in ms
        self.timer_show.timeout.connect(self.hide_all)


def uni(s):
    """
        Decode text.
    :param s: string
    :return s: string
    """

    # find and replace number to ascii character
    ascii_char = re.findall(r"\[e\]\[c\](\d+)\[p\]", s)
    for char in ascii_char:
        if char in s:
            s = s.replace(char, unichr(int(char)))

    # find and remove [*]
    other_char = re.findall(r"\[[a-z]\]+", s)
    for char in other_char:
        if char in s:
            s = s.replace(char, "")

    # find and replace html characters with unicode characters
    html_chars = {" & ": " amp ", " \" ": " quot ", " ' ": " apos ", " > ": " gt ", " < ": " lt "}
    for k, v in html_chars.items():
        if v in s:
            s = s.replace(v, k)

    return s
