# -*- coding: utf-8 -*-
import pylab
import datetime
import sklearn
from sklearn import metrics,ensemble,cluster

import os
import recognition as rec
os.system('cls')

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

  return accents

startTime = datetime.datetime.now()
print startTime

CONST_setN=150
CONST_esimators=110
CONST_depth=26
CONST_learner='RandomForestClassifier'
CONST_supvec='KMeans,2, 26 mfcc'


#Parsing,getting paths, making list
speakerInfoFile=open('speaker-info.txt')
speakerList=parse(speakerInfoFile)
f = set(speakerList)
print len(f)
