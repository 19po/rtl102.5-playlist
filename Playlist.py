from PyQt4 import QtCore, QtGui
import urllib
from xml.dom.minidom import parse
import re
import json
from time import sleep
import os

__author__ = 'postrowski'

# -*-coding: utf-8-*-


class RunVlcThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        os.system("cvlc --extraintf=http http://shoutcast.rtl.it:3010/stream/1/")
        self.terminate()


class Playlist(object):
    def __init__(self, parent):
        self.nowPlayingLabel = parent.nowPlayingLabel
        self.programLabel = parent.programLabel
        self.coverWebView = parent.coverWebView
        self.programWebView = parent.programWebView
        self.timer = parent.timer
        self.width = parent.width
        self.height = parent.height
        self.central_widget = parent.central_widget
        self.hide_ui = parent.hide_ui
        self.show_ui = parent.show_ui

    def show_info(self, data):
        # get info from json file
        artist_song, song_cover, program_speakers, program_image = '', '', '', ''
        try:
            artist_song = data["artist_name"] + '\n' + data["song_title"]
            song_cover = data["song_cover"]
            program_speakers = data["program_title"] + '\n' + data["speakers"]
            program_image = data["program_image"]
        except TypeError:
            pass

        # show (dictionary value exists) or hide (dictionary value empty) widget

        # artist name, song title
        if artist_song:
            self.nowPlayingLabel.setText(artist_song)
        else:
            self.nowPlayingLabel.hide()

        # song cover
        # if song_cover:
        #     self.coverWebView.load(QtCore.QUrl(song_cover))
        # else:
        #     self.coverWebView.hide()
        self.coverWebView.load(QtCore.QUrl(song_cover))

        # program title, speakers
        if program_speakers:
            self.programLabel.setText(program_speakers)
        else:
            self.programLabel.hide()

        # program image
        if program_image:
            self.programWebView.load(QtCore.QUrl(program_image))
        else:
            self.programWebView.hide()

        # # display data
        for k, v in data.items():
            print("{:15}{:2}{:1}".format(k, ":", v.encode('utf-8')))

    def json_change(self):
        """
            Check json file.
        """
        self.hide_ui()

        # get current information (1) and make json file
        write_info_1()
        with open('/tmp/rtl1025-playlist-1.json', 'r') as f1:
            old_data = json.load(f1)

        # wait 10 seconds
        sleep(10)

        # get current information (2) and make json file
        write_info_2()
        with open('/tmp/rtl1025-playlist-2.json', 'r') as f2:
            data = json.load(f2)

        # compare information (1) and information (2)
        # if json values was changed show ui with information
        try:
            if bool(cmp(old_data.values(), data.values())):
                # print('new')
                self.show_info(data)
                self.show_ui()
                self.central_widget.show()
                self.timer.start(20000)  # 20 seconds, display ui time in ms
            else:
                # print('old')
                self.hide_ui()
        except AttributeError:
            pass


def get_status(in_file, out_file):
    # check if VLC is turned on; get generated by VLC status.xml file
    try:
        urllib.urlretrieve(in_file, out_file)
    except IOError:
        # VLC is turned off; run VLC in separate thread
        run_vlc = RunVlcThread()
        run_vlc.start()
        # wait 10 seconds, and get generated by VLC status.xml file
        sleep(10)
        urllib.urlretrieve(in_file, out_file)


def replace_html(in_file, out_file):
    # replace html characters with xml
    with open(in_file, 'r') as fr, open(out_file, 'w') as fw:
        z = ['&lt;', '&gt;']
        x = ['<', '>']
        for line in fr.readlines():
            for i in range(len(z)):
                if z[i] in line:
                    line = line.replace(z[i], x[i])
            fw.write(line)


def uni(s):
    """
    Decode text.
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
    # open xml file, get information and make json file
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
    get_status('http://127.0.0.1:8080/requests/status.xml', '/tmp/info.xml')
    replace_html('/tmp/info.xml', '/tmp/info-1.xml')

    with open('/tmp/rtl1025-playlist-1.json', 'w') as fw:
        fw.write(json.dumps(get_xml_data('/tmp/info-1.xml')))


def write_info_2():
    get_status('http://127.0.0.1:8080/requests/status.xml', '/tmp/info.xml')
    replace_html('/tmp/info.xml', '/tmp/info-2.xml')

    with open('/tmp/rtl1025-playlist-2.json', 'w') as fw:
        fw.write(json.dumps(get_xml_data('/tmp/info-2.xml')))
