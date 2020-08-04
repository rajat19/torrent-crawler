from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='search-torrent',
    description='Search for torrents using command line',
    version='1.3.0',
    url='http://github.com/rajat19/torrent-crawler',
    download_url='https://github.com/rajat19/torrent-crawler/releases',
    author='Rajat Srivastava',
    author_email='rajatsri94@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=['pip', 'torrent', 'crawler'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'search-torrent=torrent_crawler.search:main',
        ],
    },
    install_requires=[
        'bs4',
        'requests',
        'html5lib'
    ]
)
