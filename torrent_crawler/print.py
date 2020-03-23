from torrent_crawler.color import Color
from torrent_crawler.constants import Constants


class Print:
    @staticmethod
    def bold_string(string):
        print(Color.get_bold_string(string))

    @staticmethod
    def long_hash():
        print('###########################################')

    @staticmethod
    def wrong_option():
        print(Constants.wrong_option_text)

    @staticmethod
    def colored_note(note: str):
        print('{0}Note:: {1}{2}'.format(Color.BLUE, note, Color.END))

    @staticmethod
    def option(index: int, option: str):
        print('{0}{1}: {2}{3}'.format(Color.YELLOW, index, option, Color.END))

    @staticmethod
    def thanks():
        print('\n{0}{1}{2}'.format(Color.BLUE, Constants.thanks_text, Color.END))
