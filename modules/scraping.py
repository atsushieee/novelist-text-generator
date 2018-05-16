''' scraping data '''
import requests
from bs4 import BeautifulSoup


def scraping(url):
    '''
    :param: url - objective for scraping
    '''
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup
