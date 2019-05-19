import io
import os
import requests
import sys
import subprocess
import zipfile
from torrent_crawler.color import Color
from torrent_crawler.constants import Constants


def print_wrong_option():
    print(Constants.wrong_option_text)


def get_yes_no():
    return '{0}\n{1}\n'.format(Color.get_colored_yes(), Color.get_colored_no())


def print_long_hash():
    print('###########################################')


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
        Color.BLUE, "="*block + "-"*(bar_length - block), Color.END, int(progress*100), index, total, status)
    sys.stdout.write(text)
    sys.stdout.flush()


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


def get_downloads_folder():
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


def get_zip_file(url):
    """Downloads zipped files from url"""
    r = requests.get(url)
    return zipfile.ZipFile(io.BytesIO(r.content))


def download_srt(url):
    """Downloads and extracts .srt file from zip url"""
    my_zip = get_zip_file(url)
    storage_path = get_downloads_folder()
    Color.print_bold_string(Constants.download_zip_text.format(Color.RED, storage_path, url))
    for file in my_zip.namelist():
        if my_zip.getinfo(file).filename.endswith('.srt'):
            my_zip.extract(file, storage_path)  # extract the file to current folder if it is a text file
