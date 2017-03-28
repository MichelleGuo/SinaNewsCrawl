# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import codecs
from utils import newsReader
import pandas as pd
import jieba

def data2csv():
    train_set = []
    for i in range(1,28):
        if i <10:
            file_index = '0'+str(i)
            print file_index
        else:
            file_index = str(i)
            print file_index
        train_set = newsReader(file_index,train_set)
    print "News data loads completed!"
    column = ['title','desc']
    generate_csv(train_set,column,'./data/dataSet.csv')

def generate_csv(data,cols,filename):
    # dtype=str,
    df_aux=pd.DataFrame(data,columns=cols)
    df_aux.to_csv(filename,index=True,header=True,index_label='id',encoding='utf-8')


# 去除停用词、标点符号、换行符等
def stopWord_filter(text):
    # print("filtering stopwords ... ... ")
    stopwords = codecs.open('./extraDict/stopwords.txt','r',encoding='utf8').readlines()
    stopwords = [w.strip() for w in stopwords]
    result = text.replace("\n","")
    wordlist = result.split(" ")
    for item in wordlist:
        if item in stopwords:
            wordlist.remove(item)
    string = " ".join((wordlist))
    return string


def segment():
    raw = pd.read_csv('./data/dataSet.csv',usecols=['title','desc'])
    raw['seg_content'] = ''
    seg_text = []
    for i in range(raw.shape[0]):
        content = raw.loc[i]['desc']
        content = str(content)
        content = content.strip()
        seg = jieba.cut(content,cut_all=False)
        text_str = " ".join((seg))
        text_str=stopWord_filter(text_str)
        seg_text.append(text_str)
    print "Word segment Completed!"
    raw['seg_content'] = seg_text
    col = ['title','desc','seg_content']
    generate_csv(raw,col,'./data/dataSet_seg.csv')


seg_df = pd.read_csv("./data/dataSet_seg.csv",usecols=['title','seg_content'])






