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

with open('../input/DoctoVecdata.pickle', 'rb') as handle:
  		superBagsDict = pickle.load(handle)

with open('../input/dataSentences.pickle', 'rb') as handle:
  		sentenceDict = pickle.load(handle)



def plotIterationAcc(itr,tau):
	newInstanceD = {}
	wt = np.ones(300)  # create a random weight vector

	for i in range(0,300):
		wt[i] = np.random.rand()

	for i in range(0,itr):
		 wt, newInstanceD = computeWeight(superBagsDict,Y,wt)
		 # wt, newInstanceD = computeWeightDelta(superBagsDict,Y,wt)


	pX=[]
	nX=[]
	nY=[]
	pY=[]
	FinalTweets = []

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

	print "size of finaltweets",len(FinalTweets)					
	acc=findCosineScore(FinalTweets)
	print "Accuracy=",acc
	return acc



tau = 0.07

max_tau=-1
max_itr=-1
max_acc=-1

f, axarr = plt.subplots(2, 3)

for k in range(0,2):
	for j in range(0,3):
		itr_X = []
		acc_Y = []

		for i in range(5,31,5):
			acc = plotIterationAcc(i,tau)
			itr_X.append(i)
			acc_Y.append(acc)
			if(acc>max_acc):
				max_acc=acc
				max_tau=tau
				max_itr=i
			
		axarr[k,j].plot(itr_X,acc_Y ,linestyle='-' , linewidth=1,color='red'); 
		# axarr[k,j].set_title('Tau = '+str(tau))
		# plt.show()
		tau = tau+0.01

plt.xlabel("Iterations")
plt.ylabel("Accuracy")
# plt.title('Iteration vs Accuracy (nMil using Doc2Vec) Tau=0.07-0.12')
plt.show()



print "iterations : ",max_itr
print "Accuracy :",max_acc
print "Tau ",max_tau 


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