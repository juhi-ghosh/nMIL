import pickle
import os
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from nMil import computeWeight
from nMilDelta import computeWeightDelta
import random
import matplotlib.pyplot as plt
from checkCosine import findCosineScore
from matplotlib.patches import Rectangle


#initialise input
superBagsDict = {}
Y = [1,1,-1,-1]

with open('../input/tfData.pickle', 'rb') as handle:
  		superBagsDict = pickle.load(handle)

with open('../input/tfSentence.pickle', 'rb') as handle:
  		sentenceDict = pickle.load(handle)


newInstanceD = {}
wt = np.ones(300)  # create a random weight vector
itr=2
tau=0.85




eta_X=[]
acc_Y=[]
eta=0.1
for i in range(0,13):
	
	for i in range(0,300):
		wt[i] = np.random.rand()
	for j in range(0,itr):
		wt, newInstanceD = computeWeight(eta,superBagsDict,Y,wt)
	# wt, newInstanceD = computeWeightDelta(superBagsDict,Y,wt)

	FinalTweets = []
	# Algorithm1
	for k in newInstanceD.keys():
		# print "super",k
		# print "***************************************************************8"
		for i in newInstanceD[k].keys():
			# print "bag",i
			# print "########################"
			for j in newInstanceD[k][i].keys():

				if newInstanceD[k][i][j]>=tau and Y[k-1]==1:
					#print "article: ",k,i,j
					#print "prob: ",newInstanceD[k][i][j]
					#print "sentence: ", sentenceDict[k][i][j]
					item = []
					item.append(k)
					item.append(i)
					item.append(j)
					FinalTweets.append(item)

	print "size of finaltweets",len(FinalTweets)					
	acc=findCosineScore(FinalTweets)
	print "Accuracy=",acc
	eta_X.append(eta)
	acc_Y.append(acc)
	eta=eta+0.1


plt.plot(eta_X,acc_Y ,linestyle='-' , linewidth=1,color='red'); 
plt.title('Eta vs Accuracy (nMil using TF input) ')
plt.xlabel("Eta")
plt.ylabel("Accuracy")
plt.show()


# print superBagsDict[1].keys()
# print superBagsDict[2].keys()

# plt.hist(pY,bins=100,color='b',label="Positive")
# plt.hist(nY,bins=100,color='r',label="Negative")


# p1 = Rectangle((0, 0), 1, 1, fc="b")
# p2 = Rectangle((0, 0), 1, 1, fc="r")


# plt.legend([p1, p2], ["Positive", "Negative"])
# plt.title("Estimated Probability")
# plt.xlabel("Value")
# plt.ylabel("Frequency")
# plt.show()