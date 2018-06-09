import configparser
import binascii
import os
import requests
from xml.dom import minidom

JAPANESE = "japanese"
ALPHABET = "alphabet"
SYMBOL = "symbol"



class Emoji:
    """
    f4 82 XX 81 f4 80 VV WW RRR f4 8f bf bf
    XXはフォントの種類
    hiragana = [0xac,0xb0,0xa8,0xb4] # XX   あ~ず:84 ぜ~ァ:85 ィ~ー:86 # VV
    alphabet = [0x9c,0xa0,0xa4,0x98] # XX   letter:84 # VV symbol:85 # VV
    WWは文字 #0x81~0xbf
    RRRはなんでも良い
    """
    def __init__(self, yahoo_appid):
        """

        :param yahoo_appid: Yahoo!ルビ振りapiを利用するための、Yahooデベロッパーネットワークのappid
        """
        self.ini = configparser.ConfigParser()
        self.ini.optionxform = str
        path = os.path.dirname(os.path.abspath(__file__))
        self.ini.read(path + '/table.ini', 'UTF-8')

        self.japanese = [i[0] for i in self.ini.items(JAPANESE)]
        self.alphabet = [i[0] for i in self.ini.items(ALPHABET)]
        self.symbols = [i[0] for i in self.ini.items(SYMBOL)]

        self.yahoo_appid = yahoo_appid


    def __symbol(self, string):
        s = string
        if string == '\'':
            s = 'SINGLE_QUOTE_1'
        if string == '😃':
            s = 'FACE'
        if string == '#':
            s = 'NUMBER_SIGN'
        if string == '=':
            s = 'EQUAL_SIGN'
        if string == '[':
            s = 'LEFT_SQUARE_BRACKET_1'
        if string == ']':
            s = 'RIGHT_SQUARE_BRACKET_2'
        if string == ';':
            s = 'SEMICOLON'
        if string == ':':
            s = 'COLON'

        if s in self.symbols:
            return self.ini.get('symbol', s)
        else:
            return False

    def __cast_hex(self, h):
        return hex(h)[2:]

    def __yahoo_api(self, text):
        host = 'https://jlp.yahooapis.jp/FuriganaService/V1/furigana'
        params = {'appid': self.yahoo_appid, 'grade': 1, 'sentence': text}
        response = requests.get(url=host, params=params)
        return response

    def __text_to_hiragana(self, text):
        api_result = self.__yahoo_api(text).text
        dom = minidom.parseString(api_result)
        if dom.getElementsByTagName("Error") != []:
            message = dom.getElementsByTagName("Message")
            return message[0].firstChild.data
        words = dom.getElementsByTagName("Word")
        string = ""
        for word in words:
            nodeNames = [x.nodeName for x in word.childNodes]
            if "Furigana" in nodeNames:
                for f in word.childNodes:
                    if f.nodeName == "Furigana":
                        string += f.firstChild.data
                    # if f.nodeName == "SubWordList":
                    #    word.removeChild(f)
            else:
                for f in word.childNodes:
                    if f.nodeName == "Surface":
                        string += f.firstChild.data
        return string

    def convert(self, string="Hello, World", japanese_font=0xac, alphabet_font=0x9c):
        """

        :param string: 変換したい文字列 string you want to convert
        :param japanese_font: japanese font 0xac,0xb0,0xa8,0xb4
        :param alphabet_font: alphabet and symbol font 0x9c,0xa0,0xa4,0x98
        :return: converted string
        """
        ww = ""
        output = ""
        font = None
        j_font = japanese_font
        a_font = alphabet_font
        texts = self.__text_to_hiragana(string)
        for text in texts:
            flag = False
            if text in self.japanese:
                flag, font, ww = True, j_font, self.ini.get(JAPANESE, text)
            elif text in self.alphabet:
                flag, font, ww = True, a_font, self.ini.get(ALPHABET, text)
            elif self.__symbol(text):
                flag, font, ww = True, a_font, self.__symbol(text)
            if flag is False:
                output += text
            else:
                char = "f482" + self.__cast_hex(font) + "81f480" + ww + "f48fbfbf"
                output += binascii.unhexlify(char).decode()
        return output



