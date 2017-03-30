#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import pandas as pd
import csv
from textrank4zh import TextRank4Keyword, TextRank4Sentence
# Extract keywords and abstract Chinese article

def get_all_text(df):
    document = []
    for i in range(df.shape[0]):
        string = df.loc[i][1]
        if(type(string)==str):
            string = string.strip().decode('utf-8')
            document.append(string)
    return document

def get_key_sentence(index,text,result):
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')
    # print( '摘要：' )
    abstract = []
    for item in tr4s.get_key_sentences(num=3):
        # print(item.index, item.weight, item.sentence)
        abstract.append(item.sentence)
    result.append([(index,abstract)])
    return result
    # return result
if __name__ == '__main__':
    df = pd.read_csv('../preprocess/data/dataSet.csv',usecols=['title','desc'])
    rfile = './textRank.csv'
    result = []
    doc = get_all_text(df)
    # keySentence =
    for i in range(doc.__len__()):
        result = get_key_sentence(i,doc[i],result)
    with open(rfile, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(('title','seg_content','score','sentiment'))
        for item in result:
            writer.writerows(item)

    print("work done!")

