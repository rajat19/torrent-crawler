class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def get_bold_string(string) -> str:
        return '{0}{1}{2}'.format(Color.BOLD, string, Color.END)

    @staticmethod
    def print_bold_string(string):
        print(Color.get_bold_string(string))

    @staticmethod
    def get_colored_yes() -> str:
        return '{0}y: Yes{1}'.format(Color.GREEN, Color.END)

    @staticmethod
    def get_colored_no() -> str:
        return '{0}n: No{1}'.format(Color.RED, Color.END)

    @staticmethod
    def print_colored_note(note: str):
        print('{0}Note:: {1}{2}'.format(Color.BLUE, note, Color.END))
