import requests
from bs4 import BeautifulSoup


def make_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup
