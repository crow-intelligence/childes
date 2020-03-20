import io
import zipfile
from urllib.parse import urljoin

import requests
import validators
from bs4 import BeautifulSoup

ame = "https://childes.talkbank.org/access/Eng-NA/"
bre = "https://childes.talkbank.org/access/Eng-UK/"


outpath = "data/raw"


def get_links(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("a")
    links = [urljoin(url, e["href"]) for e in links]
    links = [e for e in links if validators.url(e)]
    for link in links:
        try:
            link_html = requests.get(link).text
            link_soup = BeautifulSoup(link_html, "lxml")
            link_links = link_soup.find_all("a")
            link_links = [
                urljoin(url, e["href"])
                for e in link_links
                if "Download transcripts" in e.text
            ][0]
            r = requests.get(link_links)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(outpath)
        except Exception as e:
            continue


for e in [ame, bre]:
    get_links(e)
