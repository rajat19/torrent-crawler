[![License](https://img.shields.io/github/license/rajat19/torrent-crawler?style=for-the-badge)](https://github.com/rajat19/torrent-crawler/blob/master/LICENSE)
![Python](https://img.shields.io/pypi/pyversions/search-torrent?style=for-the-badge)
[![GitHub last commit](https://img.shields.io/github/last-commit/rajat19/torrent-crawler?style=for-the-badge)](https://github.com/rajat19/torrent-crawler/commits/master)

[![Open Issues](https://img.shields.io/github/issues-raw/rajat19/torrent-crawler?style=for-the-badge)](https://www.github.com/rajat19/torrent-crawler/issues)
[![Open PR](https://img.shields.io/github/issues-pr-raw/rajat19/torrent-crawler?label=open%20PR&style=for-the-badge)](https://github.com/rajat19/torrent-crawler/pulls)
[![Closed PR](https://img.shields.io/github/issues-pr-closed-raw/rajat19/torrent-crawler?label=closed%20PR&style=for-the-badge&color=orange)](https://github.com/rajat19/torrent-crawler/pulls?q=is%3Apr+is%3Aclosed)

## Torrent Crawler
It is not always easy to find torrents for your favourite movies, and that too while sitting at a place where torrent sites are banned on browsers. Torrent Crawler got its motivation from this issue only. Torrents can be easily downloaded along with their subtitles just by typing name of movies in terminal.

An easy way to get your favourite movie torrents. Try it now !!

> Search for torrents using CLI
```bash
pip install search-torrent
search-torrent
```

> Use api to get data (movies and subtitles)
```bash
python api.py
```

<p align="center"><img src="https://github.com/rajat19/torrent-crawler/blob/master/img/search-torrent-colorized.gif?raw=true"/></p>

---
### Contributing
```bash
git clone https://github.com/rajat19/torrent-crawler.git
cd torrent-crawler
pip install -r requirements.txt
python setup.py install
python torrent_crawler/search.py
```

---
### What's next
- Store search history in cache or something for faster processing
- Integrate kickass and piratebay for wider search results