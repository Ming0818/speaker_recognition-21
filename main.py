# -*- coding: utf-8 -*-
import pylab
import datetime
import sklearn
from sklearn import metrics,ensemble,cluster

import os
import recognition as rec
os.system('cls')

startTime = datetime.datetime.now()
print startTime

CONST_setN=150
CONST_esimators=100
CONST_depth=25
CONST_learner='RandomForestClassifier'
CONST_supvec='Kmeans-2, mfcc = 26'


#Parsing,getting paths, making list
speakerInfoFile=open('speaker-info.txt')
speakerList=rec.parse(speakerInfoFile)
print 'Parsing done',str(datetime.datetime.now()-startTime)

rightTrainList=rec.makeSublist(speakerList,0,CONST_setN)
rightTestList=rec.makeSublist(speakerList,0,20)
print 'RightSpeakerLists done',str(datetime.datetime.now()-startTime)

directory = 'wav48'
audiofiles=rec.getFiles(directory)
print "Getting files' paths done",str(datetime.datetime.now()-startTime)

trainFiles=rec.createFilesList(audiofiles,0,CONST_setN)
testFiles=rec.createFilesList(audiofiles,CONST_setN,CONST_setN+20)
print 'Files list done',str(datetime.datetime.now()-startTime)

###########################################################################
filename='results.txt'
txt = open(filename,'a')

#Supervectors, RandomForestClassifier
trainSupVec=rec.getMfcc(trainFiles)
testSupVec=rec.getMfcc(testFiles)
print 'Make supervectors done',str(datetime.datetime.now()-startTime)

clf = ensemble.RandomForestClassifier(n_estimators=CONST_esimators,
                                      max_depth=CONST_depth)
clf = clf.fit(trainSupVec, rightTrainList)
print 'RandomForestClassifier done',str(datetime.datetime.now()-startTime)



#Prediction
predictTest=clf.predict(testSupVec)
predictTrain=clf.predict(trainSupVec)
print 'Prediction done',str(datetime.datetime.now()-startTime)


#Estimation
resultTest=rec.intersec(predictTest,rightTestList)
resultTrain=rec.intersec(predictTrain,rightTrainList)
errlst=[]
for x in xrange(len(predictTest)):
  if predictTest[x]!=rightTestList[x]:
    errlst.append((rightTestList[x],predictTest[x]))

lenTrain_all,lenTrain_res,perTrain=rec.estimate(rightTrainList, resultTrain)
lenTest_all,lenTest_res,perTest=rec.estimate(rightTestList, resultTest)



#Results output
now=str(datetime.datetime.now().date())+" "+\
  str(datetime.datetime.now().time())
cond="set = "+str(CONST_setN)+\
 ", trees = "+str(CONST_esimators)+\
 ", max_depth = "+str(CONST_depth)

resTrain="Train set: size = "+str(lenTrain_all)+\
	", rigth = "+str(lenTrain_res)+", "+str(perTrain)

resTest="Test set: size = "+str(lenTest_all)+\
	", rigth = "+str(lenTest_res)+", "+str(perTest)



txt.write(now+"\n"+
          CONST_learner+"\n"+
          CONST_supvec+"\n"+
          cond+"\n"+
          resTrain+"\n"+
          resTest+"\n\n\n")

txt.close()


print 'time elapsed =', (datetime.datetime.now() - startTime)
print '\a'
