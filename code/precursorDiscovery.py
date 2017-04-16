import pickle
import os
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from nMil import computeWeight

#initialise input
superBagsDict = {}
Y = [1,1,-1,-1]

with open('../input/DoctoVecdata.pickle', 'rb') as handle:
  		superBagsDict = pickle.load(handle)

with open('../input/dataSentences.pickle', 'rb') as handle:
  		sentenceDict = pickle.load(handle)

# print superBagsDict[1].keys()
# print superBagsDict[2].keys()
newInstanceD = {}
wt = np.ones(300)  # create a random weight vector
for i in range(0,2):
	wt, newInstanceD = computeWeight(superBagsDict,Y,wt)


tau = 0.00
# Algorithm1
for k in newInstanceD.keys():
	# print "super",k
	# print "***************************************************************8"
	for i in newInstanceD[k].keys():
		# print "bag",i
		# print "########################"
		for j in newInstanceD[k][i].keys():
			# print "art",j
			# print "====================="
			if newInstanceD[k][i][j]>tau:
				print "article: ",k,i,j
				print "prob: ",newInstanceD[k][i][j]
				print "sentence: ", sentenceDict[k][i][j]

