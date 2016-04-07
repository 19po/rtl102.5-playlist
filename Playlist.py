from PyQt4 import QtCore
import urllib
from xml.dom.minidom import parse
import re
import json
from time import sleep
import os

__author__ = 'postrowski'

# -*-coding: utf-8-*-


class Playlist(object):
    """
        Class Playlist which get information and show it.
    """
    def __init__(self, parent):
        self.nowPlayingLabel = parent.nowPlayingLabel
        self.programLabel = parent.programLabel
        self.coverWebView = parent.coverWebView
        self.programWebView = parent.programWebView
        self.timer = parent.timer
        self.central_widget = parent.central_widget
        self.hide_ui = parent.hide_ui
        self.show_ui = parent.show_ui
        self.hide_all = parent.hide_all
        self.logoLabel = parent.logoLabel

    def show_info(self, data):
        """
            Print information in UI.
        :param data: json file
        :return: None
        """
        # get info from json file
        song_cover, artist_song, program_speakers, program_image = '', '', '', ''
        try:
            song_cover = data["song_cover"]
            artist_song = data["artist_name"] + '\n' + data["song_title"]
            program_speakers = data["program_title"] + '\n' + data["speakers"]
            program_image = data["program_image"]
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

        # for k, v in data.items():
        #     print("{:15}{:2}{:1}".format(k, ":", v.encode('utf-8')))

    def show_msg(self):
        """
            Resize central widget. Show UI per 20 seconds.
        :return: None
        """
        with open('/tmp/rtl1025-playlist-2.json', 'r') as f:
            data = json.load(f)

        self.show_info(data)

        # resize central widget; not smaller than fixed size
        size = self.central_widget.size()
        new_size = self.central_widget.sizeHint()
        if size < self.central_widget.resize(new_size):
            self.central_widget.resize(new_size)
        elif size > self.central_widget.resize(new_size):
            self.central_widget.resize(size)

        self.timer.start(8000)  # 8 seconds, display UI time in ms
        self.timer.timeout.connect(self.hide_all)

    def cmp_json(self, j1, j2):
        """
            Compare two json files and show message if they are different.
        :param j1: first json file
        :param j2: second json file
        :return: None
        """
        try:
            with open(j1, 'r') as f1, open(j2, 'r') as f2:
                d1 = json.load(f1)
                d2 = json.load(f2)
                if bool(cmp(d1, d2)):
                    self.show_msg()
                else:
                    self.hide_ui()
        except AttributeError:
            pass

    def json_change(self):
        """
            Get information from VLC status.xml file and compare them.
        :return: None
        """
        if os.path.exists('/tmp/rtl1025-playlist-2.json'):  # check if path exist
            with open('/tmp/rtl1025-playlist-2.json', 'r') as fr:
                d = json.load(fr)
                if d["program_title"]:  # check if dictionary item have value
                    # get current information and make json file
                    print "1111"
                    write_info_1()  # create 'rtl1025-playlist-1.json' file
                    sleep(10)  # wait 10 seconds
                    write_info_2()  # create 'rtl1025-playlist-2.json' file
                    self.cmp_json('/tmp/rtl1025-playlist-1.json', '/tmp/rtl1025-playlist-2.json')
                    return
                else:
                    print "empty"
                    return
        else:
            print "0000"
            write_info_2()  # create 'rtl1025-playlist-2.json' file
            self.show_msg()  # show message

    @staticmethod
    def remove_file():
        """
            Remove 'rtl1025-playlist-2.json' file if application was launched next time before restart system.
        :return: None
        """
        f = '/tmp/rtl1025-playlist-2.json'
        if os.path.exists(f):
            os.remove(f)


def replace_html(in_file, out_file):
    """
        Escaping xml character data.
    :param in_file: downloaded VLC status.xml as info.xml
    :param out_file: info-x.xml without xml character data
    :return: None
    """
    with open(in_file, 'r') as fr, open(out_file, 'w') as fw:
        z = ['&lt;', '&gt;', '&amp;', '&apos;', '&quot;']
        x = ['<', '>', '&', "'", '"']
        for line in fr.readlines():
            for i in range(len(z)):
                if z[i] in line:
                    line = line.replace(z[i], x[i])
            fw.write(line)


def uni(s):
    """
        Decode text downloaded from VLC status.xml.
    :param s: input string
    """
    ascii_char = re.findall(r'\[e\]\[c\](\d+)\[p\]', s)
    other_char = re.findall(r'\[[a-z]\]+', s)

    # find and replace number to ascii character
    for char in ascii_char:
        if char in s:
            s = s.replace(char, unichr(int(char)))

    # find and remove [*]
    for char in other_char:
        if char in s:
            s = s.replace(char, '')

    return s


def get_xml_data(in_file):
    """
        Open VLC status.xml file file and get information and make json file.
    :param in_file: info-x.xml without xml character data
    :return: dictionary with current information
    """
    with open(in_file, 'r') as fr:
        dom = parse(fr)
        node = dom.childNodes

        info_dict = {"program_title": "", "speakers": "", "program_image": "",
                     "artist_name": "", "song_title": "", "song_cover": ""}

        try:
            info_dict["program_title"] = uni(node[0].getElementsByTagName('prg_title')[0].firstChild.data)
            info_dict["speakers"] = uni(node[0].getElementsByTagName('speakers')[0].firstChild.data)
            info_dict["program_image"] = node[0].getElementsByTagName('image170')[0].firstChild.data

            info_dict["artist_name"] = uni(node[0].getElementsByTagName('mus_art_name')[0].firstChild.data)
            info_dict["song_title"] = uni(node[0].getElementsByTagName('mus_sng_title')[0].firstChild.data)
            info_dict["song_cover"] = node[0].getElementsByTagName('mus_sng_itunescoverbig')[0].firstChild.data
        except (IndexError, AttributeError):
            pass

        return info_dict


def write_info_1():
    """
        Get VLC status.xml file and create json file.
    :return: None
    """
    urllib.urlretrieve('http://127.0.0.1:8080/requests/status.xml', '/tmp/info.xml')
    replace_html('/tmp/info.xml', '/tmp/info-1.xml')

    with open('/tmp/rtl1025-playlist-1.json', 'w') as fw:
        fw.write(json.dumps(get_xml_data('/tmp/info-1.xml')))


def write_info_2():
    """
        Get VLC status.xml file and create json file.
    :return: None
    """
    urllib.urlretrieve('http://127.0.0.1:8080/requests/status.xml', '/tmp/info.xml')
    replace_html('/tmp/info.xml', '/tmp/info-2.xml')

    with open('/tmp/rtl1025-playlist-2.json', 'w') as fw:
        fw.write(json.dumps(get_xml_data('/tmp/info-2.xml')))
