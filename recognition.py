# -*- coding: utf-8 -*-
import os
import sklearn
from sklearn.cluster import KMeans,MiniBatchKMeans
from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
from sklearn import mixture
import numpy as np

def parse(inputFile):
  """
  Parsing input file into dictionary
  :param inputFile: lines like "225  23  F    English    Southern England"
  :return outputDict:list of No. of speakers
  temp(dictionary like {id:(age, gender, accents, region)}
  Sometimes there is no region)
  """
  indexes=[]
  genders=[]
  ages=[]
  accents=[]
  regions=[]

  for inputString in inputFile:
    text=''
    symbol = 0
    #Indexes
    while symbol < 3 and inputString[symbol]!=' ' and inputString[symbol]!='\n':
      text+=inputString[symbol]
      symbol+=1
    indexes.append(int(text))

    #Ages
    symbol += 2
    text = inputString[symbol]
    symbol += 1
    text +=inputString[symbol]
    ages.append(int(text))

    #Genders
    symbol += 3
    text = inputString[symbol]
    genders.append(text)

    #Accents
    symbol +=5
    text=''
    while inputString[symbol]!=' ' and inputString[symbol]!='\n':
      text+=inputString[symbol]
      symbol+=1
    accents.append(text)

    #Region
    text=''
    if(inputString[symbol]!='\n'):
      while inputString[symbol]==' ':
        symbol+=1
      while (inputString[symbol]!='\n'):
        text+=inputString[symbol]
        symbol+=1
    regions.append(text)
  #zipped_list = zip(ages, genders, accents, regions)
  #liswit = zip(indexes, zipped_list)
  #outputDict = dict(liswit)

  return indexes

def getFiles(directory):
  """
  Collecting paths to .wav files into one list
  :param directory: path to direcrory
  :return audiofiles: list with paths "wav48/<speaker No>/<speaker No>_<sentence No>
  """
  audiofiles = []
  lenghs=[]
  for d, dirs, files in os.walk(directory):
    files1=[]
    for onefile in files:
      files1.append(d+"/"+onefile)
    audiofiles.append(files1)
  audiofiles.pop(0)
  return audiofiles

def createFilesList(audiofiles, startingFrom, stopAt):
  """
  Divide list into parts
  :param audiofiles: list of paths
  :return trainSet: list of paths
  Sometimes there is no region
  """
  trainSet = []
  for files in audiofiles:
    subSet=[]
    for index in xrange(startingFrom, stopAt):
      subSet.append(files[index])
    trainSet.append(subSet)
  return trainSet

def makeSuperVecAver(path_to_onefile):
  """
  Making supervector using average values
  :param path_to_onefile: path to file
  :return aver_vec: list of numbers-supervector of mfcc (average)
  """
  aver_vec=[]
  (rate,sig)=wav.read(path_to_onefile)
  mfcc_feat=mfcc(sig,rate,numcep=13)
  aver_elem=[0 for x in xrange(len(mfcc_feat[0]))]
  for vec in mfcc_feat:
    aver_elem+=vec
  aver_vec=aver_elem/len(mfcc_feat)
  return aver_vec


def makeSuperVecKMean(path_to_onefile):
  """
  Making supervector using average values
  :param path_to_onefile: path to file
  :return aver_vec: list of numbers-supervector of mfcc (average)
  """
  clf = KMeans(n_clusters=2)
  (rate,sig)=wav.read(path_to_onefile)
  mfcc_feat=mfcc(sig,rate,numcep=26)
  clf.fit(mfcc_feat)
  aver_vec = listmerge(clf.cluster_centers_)
  return aver_vec

def getMfcc(filesArray):
  """
  Making list of supervector
  :param filesArray: array of paths to files
  :return aver_array: list of numbers-supervector of mfcc (average)
  """
  aver_array=[]
  for vec in filesArray:
    for onefile in vec:
      aver_vec=makeSuperVecKMean(onefile)
      aver_array.append(aver_vec)
  return aver_array

def intersec(predict, right):
  result=[]
  for i in xrange(len(predict)):
    if(predict[i]==right[i]):
      result.append(predict[i])
  return result

def makeSublist(biglst, startingFrom, stopAt):
  reslst=[]
  for speaker in biglst:
    for i in xrange(startingFrom, stopAt):
      reslst.append(speaker)
  return reslst

def estimate(right, res):
  len_all=len(right)
  len_res=len(res)
  per=(float(len_res)/len_all)*100
  return len_all,len_res,per

def listmerge(lstlst):
  all=[]
  for lst in lstlst:
    all.extend(lst)
  return all
