# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import pandas as pd
import csv


def loadTxt(filePath):
    content=[]
    with open(filePath,'r') as fopen:
        for item in fopen:
            content.append(item.strip("\n"))
    return content

def load_degreeDict():
    degree_path = "./extraDict/degree/"
    mostDict = loadTxt(degree_path+'most.txt')
    veryDict = loadTxt(degree_path+'very.txt')
    moreDict = loadTxt(degree_path+'more.txt')
    ishDict = loadTxt(degree_path+'ish.txt')
    insufficientDict = loadTxt(degree_path+'insufficiently.txt')
    inverseDict = loadTxt(degree_path+'inverse.txt')
    return mostDict,veryDict,moreDict,ishDict,insufficientDict,inverseDict

dictionary_path = "./extraDict/sentiment/"
posDict = loadTxt(dictionary_path+"ntusd-positive.txt")
negDict = loadTxt(dictionary_path+"ntusd-negative.txt")
mostDict,veryDict,moreDict,ishDict,insufficientDict,inverseDict = load_degreeDict()


def degree_grain(word,sentiment_value):
     # 如果有程度副词
    if word in mostDict:
        sentiment_value *=2
    elif word in veryDict:
        sentiment_value *=1.5
    elif word in moreDict:
        sentiment_value *= 1.25
    elif word in ishDict:
        sentiment_value *= 0.5
    elif word in insufficientDict:
        sentiment_value *= 0.25
    elif word in inverseDict:
        # 如果有否定词
        sentiment_value *= -1
    return  sentiment_value

def reformScore(posScore,negScore):
    pos =0
    neg =0
    if posScore<0 and negScore>=0:
        neg = negScore - posScore
        pos = 0
    elif posScore>=0 and negScore<0:
        pos = posScore - negScore
        neg = 0
    elif posScore<0 and negScore<0:
        pos = -posScore
        neg = -negScore
    else:
        pos = posScore
        neg = negScore
    return [pos,neg]


def scoreNorm(scoreList):
    scoreArray = np.array(scoreList)
    pos = np.sum(scoreArray[:,0])
    neg = np.sum(scoreArray[:,1])
    avgPos = np.mean(scoreArray[:,0])
    avgNeg = np.mean(scoreArray[:,1])
    return [pos,neg,avgPos,avgNeg]


def compute_sentence_score(news_content):
    # 单句得分
    single_sentence_score=[]
    senList = news_content.split("。")
    content_score=0
    # 遍历已经分词完的句子中的单词item
    for item in senList:
         wordList = item.split(" ")
         # wordPosition 当前词位置
         wp = 0
         # sentiPosition 情感词位置
         sp = 0
         posScore =0
         negScore =0
         for word in wordList:
             # 如果该词为正面情感词
             if word in posDict:
                 # 直接添加正面情感得分
                 posScore +=1
                 # print(word + "pos")
                 for word1 in wordList[sp:wp]:
                     # 判断该情感词与下一情感词之间是否有否定词或程度副词
                     posScore = degree_grain(word1,posScore)
                 sp = wp+1
             # 如果该词为负面情感词
             elif word in negDict:
                 # 直接添加负面情感得分
                 negScore +=1
                 # print(word + "neg")
                 for word2 in wordList[sp:wp]:
                     negScore = degree_grain(word2,negScore)
                 sp = wp+1
             elif word == "!" or word == "！":
                 for word3 in wordList[::-1]:
                     if word3 in posDict:
                         posScore +=2
                         break
                     elif word3 in negDict:
                         negScore +=2
                         break
             wp+=1
         single_sentence_score.append(reformScore(posScore,negScore))
         content_score = scoreNorm(single_sentence_score)
    return content_score

def senti_judge(scorelist):
    pos = 1
    neg = -1
    neu = 0
    if scorelist[0] > scorelist[1]:
        value = pos
    elif scorelist[0] < scorelist[1]:
        value = neg
    else:
        value =neu
    return value

def compute_all(df):
    result=[]
    for i in range(df.shape[0]):
        if(type(df.loc[i][3])==str):
            sentiScore = compute_sentence_score(df.loc[i][3])
            sentiValue = senti_judge(sentiScore)
            result.append([(df.loc[i][0], df.loc[i][1], df.loc[i][2], sentiScore,sentiValue)])
        else:
            result.append([(df.loc[i][0], df.loc[i][1], df.loc[i][2], 0,0)])
    return result

# 写入新的csv中
def get_result(datafile,resultfile):
    df = pd.read_csv(datafile)
    rows = compute_all(df)
    with open(resultfile, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(('title','seg_content','score','sentiment'))
        for item in rows:
            writer.writerows(item)
    print("sentiment done!")


if __name__ == '__main__':
    fname = './data/dataSet_seg.csv'
    rname = './data/resultSet.csv'
    # inputfile, outpufile
    get_result(fname,rname)
    print "work done!"


