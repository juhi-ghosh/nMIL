import pickle
import os
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from nMil import computeWeight
import random
import matplotlib.pyplot as plt
from checkCosine import findCosineScore
from matplotlib.patches import Rectangle


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

for i in range(0,300):
	wt[i] = np.random.rand()

for i in range(0,20):
	wt, newInstanceD = computeWeight(superBagsDict,Y,wt)


pX=[]
nX=[]
nY=[]
pY=[]
FinalTweets = []

tau = 0.11
cntP=1
cntN=1
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
			if Y[k-1]==1:
				pX.append(cntP)
				pY.append(newInstanceD[k][i][j])
				cntP=cntP+1
			else:
				nX.append(cntN)
				nY.append(newInstanceD[k][i][j])
				cntN=cntN+1

			if newInstanceD[k][i][j]>=tau and Y[k-1]==1:
				#print "article: ",k,i,j
				#print "prob: ",newInstanceD[k][i][j]
				#print "sentence: ", sentenceDict[k][i][j]
				item = []
				item.append(k)
				item.append(i)
				item.append(j)
				FinalTweets.append(item)



acc=findCosineScore(FinalTweets)
print "Accuracy=",acc

plt.hist(pY,bins=100,color='b',label="Positive")
plt.hist(nY,bins=100,color='r',label="Negative")


p1 = Rectangle((0, 0), 1, 1, fc="b")
p2 = Rectangle((0, 0), 1, 1, fc="r")


plt.legend([p1, p2], ["Positive", "Negative"])
plt.title("Estimated Probability")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()


