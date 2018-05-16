''' speech-of-text '''
from manipulate_db import select_records
import MeCab

DB_FILE_PATHS = '../db/data.db'
TABLE_NAME = 'books'
EXTRACTED_COLUMN = 'contents'
MECAB_TAGGER = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'


if __name__ == '__main__':
    analyzedTextArray = select_records(DB_FILE_PATHS, TABLE_NAME, EXTRACTED_COLUMN, 'WHERE id=189')

    mecab = MeCab.Tagger(MECAB_TAGGER)
    mecab.parse('')
    for analyzedText in analyzedTextArray:
        node = mecab.parseToNode(analyzedText[0])

        while node:
            # node_array = node.feature.split('------')
            # if node_array[0] == '名詞' and node_array[1] != '数':
            #     words.append(node.surface)
            # elif node_array[0] == '動詞' or node_array[0] == '形容詞' or node_array[0] == '連体詞':
            #     words.append(node_array[6]) if node_array[6] != '*' else None

            featureArray = node.feature.split(',')
            print(node.surface, featureArray)
            node = node.next
