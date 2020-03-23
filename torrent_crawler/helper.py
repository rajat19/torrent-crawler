import io
import os
import requests
import sys
import subprocess
import zipfile
from torrent_crawler.color import Color
from torrent_crawler.constants import Constants
from torrent_crawler.print import Print


class Helper:
    @staticmethod
    def ask_for_options() -> bool:
        while True:
            want = input(Color.get_yes_no())
            if want in ['y', 'Y']:
                return True
            if want in ['n', 'N']:
                return False
            Print.wrong_option()
            continue

    @staticmethod
    def take_input(input_type, options):
        if input_type not in Constants.input_types:
            Print.bold_string('Wrong input type: {0}'.format(input_type))
            exit(1)
        specific_text = Constants.specific_text[input_type]
        no_of_options = len(options)
        Print.bold_string(specific_text)
        for i in range(1, len(options)):
            Print.option(i, options[i])
        while True:
            index = int(input())
            if 1 <= index <= no_of_options:
                break
            else:
                Print.wrong_option()
                continue
        return options[index-1]

    @staticmethod
    def take_optional_input(input_type):
        Print.long_hash()
        if input_type not in Constants.input_types:
            Print.bold_string('Wrong input type: {0}'.format(input_type))
            exit(1)
        selection_text = Constants.selection_text[input_type]
        specific_final_option = Constants.specific_final_option[input_type]
        special_final_option = Constants.special_final_option[input_type]
        Print.bold_string(selection_text)
        want = Helper.ask_for_options()
        index = 0
        options = Constants.options[input_type]
        if not want:
            Print.colored_note(special_final_option)
            return options[0]
        final_option = Helper.take_input(options)
        Print.colored_note(specific_final_option.format(options[index]))
        return final_option

    @staticmethod
    def update_progress(index, total):
        """Show update progress for index out of total"""
        bar_length = 30
        status = ""
        progress = index / total
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        block = int(round(bar_length * progress))
        text = "\rCrawling like a snake: {0}[{1}]{2} {3}% [{4}/{5}] {6}".format(
            Color.BLUE, "=" * block + "-" * (bar_length - block), Color.END, int(progress * 100), index, total, status)
        sys.stdout.write(text)
        sys.stdout.flush()

    @staticmethod
    def open_magnet_link(magnet):
        """Opens magnet link"""
        if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            os.startfile(magnet)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.Popen(['xdg-open', magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def __get_downloads_folder():
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads', 'subtitles')

    @staticmethod
    def __get_zip_file(url):
        """Downloads zipped files from url"""
        r = requests.get(url)
        return zipfile.ZipFile(io.BytesIO(r.content))

    @staticmethod
    def download_srt(url):
        """Downloads and extracts .srt file from zip url"""
        my_zip = Helper.__get_zip_file(url)
        storage_path = Helper.__get_downloads_folder()
        Print.bold_string(Constants.download_zip_text.format(Color.RED, storage_path, url))
        for file in my_zip.namelist():
            if my_zip.getinfo(file).filename.endswith('.srt'):
                my_zip.extract(file, storage_path)  # extract the file to current folder if it is a text file
