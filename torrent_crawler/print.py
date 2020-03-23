from torrent_crawler.color import Color
from torrent_crawler.constants import Constants


class Print:
    @staticmethod
    def print_bold_string(string):
        print(Color.get_bold_string(string))

    @staticmethod
    def print_long_hash():
        print('###########################################')

    @staticmethod
    def print_wrong_option():
        print(Constants.wrong_option_text)

    @staticmethod
    def print_colored_note(note: str):
        print('{0}Note:: {1}{2}'.format(Color.BLUE, note, Color.END))

    @staticmethod
    def print_option(index: int, option: str):
        print('{0}{1}: {2}{3}'.format(Color.YELLOW, index, option, Color.END))

    @staticmethod
    def print_thanks():
        print('\n{0}{1}{2}'.format(Color.BLUE, Constants.thanks_text, Color.END))
