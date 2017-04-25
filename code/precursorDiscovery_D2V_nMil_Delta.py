import pickle
import os
import numpy as np
import sys
import math
import matplotlib.mlab as mlab
reload(sys)
sys.setdefaultencoding('utf8')
from nMil import computeWeight
from nMilDelta import computeWeightDelta
import random
import matplotlib.pyplot as plt
from checkCosine import findCosineScore
from matplotlib.patches import Rectangle


def graph_est_Prob(pY,nY):
	plt.hist(pY,bins=100,color='b',label="Positive")
	plt.hist(nY,bins=100,color='r',label="Negative")


	p1 = Rectangle((0, 0), 1, 1, fc="b")
	p2 = Rectangle((0, 0), 1, 1, fc="r")
	# plt.axis([0, 1200, 0, 0.25])


	plt.legend([p1, p2], ["Positive", "Negative"])
	plt.title("Estimated Probability using nMIL Algorithm")
	plt.xlabel("Probability Range Value")
	plt.ylabel("Frequency(No. of Articles)")
	plt.show()

# plotting a graph
def graph_cos_days(day_cos_selprec_list):
	
	d = len(day_cos_selprec_list)
	
	days = [i+1 for i in range(d)]

	# print day_cos_selprec_list
	#print days

	plt.plot(days, day_cos_selprec_list , 'bo', linestyle= '-')
	plt.axis([0, 11, 0, 1.2])

	font = {'family': 'serif',
		'color':  'darkred',
		'weight': 'normal',
		'size': 14,
		}

	plt.title('Mean of Relative Cosine Values w.r.t. Target Events in History Days\n (using nMIL Algorithm)\n')
	plt.xlabel("History Days")
	plt.ylabel("Precursors Cosine Similarity Score")
	plt.show()

def graph_cos_prob(day_cos_list,all_cos_list, day_prob_list, all_prob_list):

	font = {'family': 'serif',
		'color':  'darkred',
		'weight': 'normal',
		'size': 14,
		}

	d = len(all_prob_list)
	days1 = [i+1 for i in range(d)]
	d = len(all_cos_list)
	days2 = [i+1 for i in range(d)]

	
	plt.title('Distribution of Relative Cosine Similarity using nMIL Algorithm\n')
	plt.xlabel("Day-wise Articles")
	plt.ylabel("Probability Density                     Cosine Similarity")
	plt.plot( days1,all_prob_list, 'go', linestyle= '-')
	plt.plot( days2,all_cos_list, 'bo', linestyle= '-')

	#plotting for all articles
	plt.show()

	
	d = len(day_prob_list)
	days3 = [i+1 for i in range(d)]
	d = len(day_cos_list)
	days4 = [i+1 for i in range(d)]

	plt.plot( days3,day_prob_list, 'ro', linestyle= '-')
	plt.plot( days4,day_cos_list, 'yo', linestyle= '-')

	plt.xlabel("Day-wise Articles (tau = 0.11)")
	plt.title('Distribution of Relative Cosine Similarity using nMIL Algorithm\n')
	plt.xlabel("Day-wise Articles")
	plt.ylabel("Probability Density                     Cosine Similarity")
	#plotting for only precursors
	plt.show()



#initialise input
superBagsDict = {}
Y = [1,1,-1,-1]

with open('../input/DoctoVecdata.pickle', 'rb') as handle:
  		superBagsDict = pickle.load(handle)

with open('../input/dataSentences.pickle', 'rb') as handle:
  		sentenceDict = pickle.load(handle)

newInstanceD = {}
wt = np.ones(300)  # create a random weight vector

for i in range(0,300):
		wt[i] = np.random.rand()

eta=0.8

for i in range(0,5):
	wt, newInstanceD = computeWeightDelta(eta,superBagsDict,Y,wt)


pX=[]
nX=[]
nY=[]
pY=[]
FinalTweets = []

tau = 0.115
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
				# print "prob: ",newInstanceD[k][i][j]
				# print "sentence: ", sentenceDict[k][i][j]
				item = []
				item.append(k)
				item.append(i)
				item.append(j)
				FinalTweets.append(item)



acc, day_cos_selprec_list, all_cos_list, all_prob_list, day_prob_list, day_cos_list = findCosineScore(FinalTweets, newInstanceD)
print "Accuracy=",acc
graph_cos_days(day_cos_selprec_list)
graph_cos_prob(day_cos_list,all_cos_list, day_prob_list, all_prob_list)
graph_est_Prob(pY,nY)

