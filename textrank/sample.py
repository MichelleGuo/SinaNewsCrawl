#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
import pandas as pd
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def get_all_text(df):
    document = []
    for i in range(df.shape[0]):
        string = df.loc[i][1]
        if(type(string)==str):
            string = string.strip().decode('utf-8')
            document.append(string)
    return document

def get_key_sentence(text):
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')
    result = ''
    print( '摘要：' )
    for item in tr4s.get_key_sentences(num=3):
        print(item.index, item.weight, item.sentence)
        # result.append(item.sentence)
    # return result
if __name__ == '__main__':
    df = pd.read_csv('../preprocess/data/dataSet.csv',usecols=['title','desc'])
    result = []
    doc = get_all_text(df)
    # keySentence =
    for i in range(doc.__len__()):
        get_key_sentence(doc[i])

