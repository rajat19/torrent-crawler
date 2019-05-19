from bs4 import BeautifulSoup
import requests
from torrent_crawler.color import Color
from torrent_crawler.constants import Constants
from torrent_crawler.helper import download_srt, print_wrong_option


class Subtitle:
    @staticmethod
    def get_search_url(search_term, page_no):
        q = search_term
        if page_no > 2:
            q += page_no
        return Constants.subtitle_search_url.format(q)

    def crawl_list(self, search_term):
        page_no = 1
        has_next_page = True
        while has_next_page:
            url = self.get_search_url(search_term, page_no)
            req = requests.get(url)
            soup = BeautifulSoup(req.text, features='html5lib')
            media_list = soup.find_all('li', {'class': 'media-movie-clickable'})
            for media in media_list:
                media_body = media.find('div', {'class': 'media-body'})
                media_link = media_body.find('a').get('href')
                media_name = media.find('h3', {'class': 'media-heading'}).text

    @staticmethod
    def crawl_movie(url):
        req = requests.get(url)
        soup = BeautifulSoup(req.text, features='html5lib')
        subtitle_table = soup.find('table', {'class': 'other-subs'}).find('tbody').find_all('tr')
        subtitles = {}
        subtitle_languages = []
        for subtitle in subtitle_table:
            rating = subtitle.find('td', {'class': 'rating-cell'}).text
            language = subtitle.find('td', {'class': 'flag-cell'})\
                .find('span', {'class': 'sub-lang'}).text
            download_link = subtitle.find('a').get('href').replace('/subtitles/', 'subtitle/')
            link = Constants.subtitle_base_url.format(download_link + '.zip')
            subtitle_languages.append(language)
            if language not in subtitles:
                subtitles[language] = []
            subtitles[language].append({
                'rating': rating,
                'link': link
            })
        return subtitles

    @staticmethod
    def take_language_input(languages):
        Color.print_bold_string(Constants.subtitle_language_text)
        for i in range(len(languages)):
            print('{0}{1}: {2}{3}'.format(Color.YELLOW, i+1, languages[i], Color.END))
        while True:
            lang = int(input())
            if 1 <= lang <= len(languages):
                break
            else:
                print_wrong_option()
                continue
        return languages[lang-1]

    def search_subtitle(self, url):
        subtitles = self.crawl_movie(url)
        lang = self.take_language_input(list(subtitles.keys()))
        # Download first subtitle for that language as it is highest rated
        subtitle_link = subtitles[lang][0]['link']
        download_srt(subtitle_link)


if __name__ == '__main__':
    s = Subtitle()
    s.search_subtitle('tt4154756')
