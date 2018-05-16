''' scraping works' data -> store them into DB '''
import time
from modules.manipulate_db import create_db, create_table, add_dict
from modules.scraping import scraping

ROOT_URL = 'https://www.aozora.gr.jp'
AUTHOR_URL = '/cards/000035/'

MAIN_URL = ROOT_URL + '/index_pages/person35.html'
subUrlList = []
contentsUrlList = []
bookDict = {}

DB_FILE_PATHS = 'db/data.db'
TABLE_NAME = 'books'
SCHEME = '(id INTEGER PRIMARY KEY, title text, contents text)'


if __name__ == '__main__':
    # an author's url => works' url array
    authorSoup = scraping(MAIN_URL)
    authorWorks = authorSoup.find('ol').find_all('li')
    for work in authorWorks:
        # eliminate works which is written in '旧字旧仮名'
        tagContents = str(work)
        if '旧字旧仮名' in tagContents:
            continue

        workUrl = work.a['href']
        workUrl = workUrl.replace('..', ROOT_URL)
        subUrlList.append(workUrl)

    # works' url array => detail page array
    for idx, subUrl in enumerate(subUrlList):
        print(idx + 1, subUrl)
        workSoup = scraping(subUrl)
        if workSoup.find('a', text='いますぐXHTML版で読む'):
            workUrl = workSoup.find('a', text='いますぐXHTML版で読む')['href']
            workUrl = workUrl.replace('./', ROOT_URL + AUTHOR_URL)
            contentsUrlList.append(workUrl)
            time.sleep(1)

    # detail page array => title and contents
    for idx, contentsUrl in enumerate(contentsUrlList):
        print(idx + 1, contentsUrl)
        detailSoup = scraping(contentsUrl)

        # eliminate the ruby parts
        rtNum = len(detailSoup.find_all('rt'))
        rpNum = rtNum * 2
        for x in range(rtNum):
            detailSoup.rt.decompose()
        for x in range(rpNum):
            detailSoup.rp.decompose()

        detailTitle = detailSoup.find('h1').get_text()
        detailContents = detailSoup.find('div', class_='main_text').get_text()
        print(detailContents)
        bookDict[detailTitle] = detailContents
        time.sleep(1)

    # create db file and table
    create_db(DB_FILE_PATHS)
    create_table(DB_FILE_PATHS, TABLE_NAME, SCHEME)

    # add books info into [books] table
    add_dict(DB_FILE_PATHS, TABLE_NAME, bookDict)
