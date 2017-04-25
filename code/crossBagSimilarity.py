#!/usr/bin/python
import pickle
import os
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import random
import math

m0=0.5
p0=0.5
beta=3.0
lamda=0.05




def cosineSimilarity(v1, v2):
    
   v1 = np.array(v1)
   v2 = np.array(v2)
   prod = np.dot(v1, v2)
   len1 = math.sqrt(np.dot(v1, v1))
   len2 = math.sqrt(np.dot(v2, v2))
   return prod / (len1 * len2)*1.0


def getSimilarity(day1,day2): #maps of day1 and day2
	
	total = 0
	n=0
	for i in day1.keys():
		for j in day2.keys():
			sim = cosineSimilarity(day1[i],day2[j])
			total  = total + sim
			n=n+1			

	return (total*1.0/n)


with open('../input/DoctoVecdata.pickle', 'rb') as handle:
	superBagsDict = pickle.load(handle)

pairWiseDict = {}

for i in superBagsDict.keys():
	
	bagsDict = {}

	print "superbag ",i
	bagsDict[1] = 1

	for j in range(2,6):

		print "bag j",j, len(superBagsDict[i][j]), " bag j-1 ",len(superBagsDict[i][j-1])
		bagsDict[j] = getSimilarity(superBagsDict[i][j],superBagsDict[i][j-1])

	pairWiseDict[i] = bagsDict


print pairWiseDict

with open('../input/crossBagSimilarity.pickle', 'wb') as handle:
		pickle.dump(pairWiseDict, handle)
