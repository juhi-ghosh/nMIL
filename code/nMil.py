#!/usr/bin/python

import numpy as np
import random

m0=0.5
p0=0.5
beta=3.0
lamda=0.05


def getSign(z):
	return np.sign(z)

def sigmoid(z):
	return 1.0/(1.0+np.exp(-z))


#calculate probabality for each doc2vec arcticle
def get_pij(wt,xij):
	prod = np.dot(wt.T,xij)
	return sigmoid(prod)


def get_oij(wt,xij,pij):

	sgn = getSign(pij-p0)
	sgn = sgn * np.dot(wt.T,xij)

	if(sgn<m0):
		return 1
	else:
		return 0



#calulate mean of instances for a bag
def get_Pi(bagD):
	
	n = len(bagD)
	sums=0
	for val in bagD.values():
		sums=sums+val

	return sums/float(n)

#calculate mean of bags for a super bag
def get_P(bagD):
	n = len(bagD)
	sums=0
	for val in bagD.values():
		sums=sums+val


	return sums/float(n)


#dictionary structure for instance level probabilities
def inst_pij(wt,inputD):

	outputD={}
	for k in inputD.keys():
		# print "super",k
		# print "***************************************************************8"
		outputD[k]={}
		for i in inputD[k].keys():
			# print "bag",i
			# print "########################"
			outputD[k][i]={}
			for j in inputD[k][i].keys():
				# print "art",j
				# print "====================="
				outputD[k][i][j] = get_pij(wt,inputD[k][i][j])

	return outputD

#dictionary structure for bag level probabilities
def bag_Pi(instanceD):
	### return dictionary of bag probability
	bagD= {}

	for k in instanceD.keys():
		bagD[k]={}
		for i in instanceD[k].keys():
			bagD[k][i] = get_Pi(instanceD[k][i])


	return bagD


def superbag_P(bagD):
	## return dictionary of super bag
	superBagD={}

	for k in bagD:
		superBagD[k]=get_P(bagD[k])


	return superBagD


def computeTerm2(r,superbagD,instanceD,inputD,y):  

	t = len(instanceD[r])
	P = superbagD[r]
	Y=y[r-1]

	part1  = (Y-P)/float((P*(1-P)))
	part1 = part1 * beta / float(t)

	part2 = 0

	sum_bag = 0 

	for i in instanceD[r].keys():  # i is bags , r is a randonly chosen super bag

		sum_inst = 0
		n = 0
		for j in instanceD[r][i].keys(): # j is an article in bag i

			pij = instanceD[r][i][j]

			temp = pij * (1 - pij) * inputD[r][i][j]
			sum_inst = sum_inst + temp
			n = n + 1

		sum_inst = sum_inst/float(n)		

		sum_bag = sum_bag + sum_inst	

	part2 = sum_bag

	return part1*part2


def computeTerm3(r,superbagD,bagD,instanceD,inputD):

	t = len(instanceD[r])
	P = superbagD[r]

	
	sum_bag = 0 

	for i in instanceD[r].keys():  # i is bags , r is a randonly chosen super bag

		Pi = bagD[r][i]
		Pi1 = 0
		if i-1 >0 :
			Pi1 = bagD[r][i-1]

		sum_inst = 0
		n = 0

		for j in instanceD[r][i].keys(): # j is an article in bag i

			pij = instanceD[r][i][j]

			temp = pij * (1 - pij) * inputD[r][i][j]
			sum_inst = sum_inst + temp
			n = n + 1

		sum_inst = sum_inst/float(n)
		sum_bag = sum_bag + (2 * (Pi - Pi1 ) * sum_inst)

	sum_bag = sum_bag / float(t)

	return sum_bag



def computeTerm4(r,superbagD,bagD,instanceD,inputD):

	t = len(instanceD[r])
	P = superbagD[r]

	
	sum_bag = 0 

	for i in instanceD[r].keys():  # i is bags , r is a randonly chosen super bag

		Pi = bagD[r][i]
		Pi1 = 0
		if i-1 >0 :
			Pi1 = bagD[r][i-1]

		sum_inst = 0
		n = 0

		if(i-1==0):
			continue

		for j in instanceD[r][i-1].keys(): # j is an article in bag i

			pij = instanceD[r][i-1][j]

			temp = pij * (1 - pij) * inputD[r][i-1][j]
			sum_inst = sum_inst + temp
			n = n + 1

		
		sum_inst = sum_inst/float(n)
		

		sum_bag = sum_bag + (2 * (Pi - Pi1 ) * sum_inst)

	sum_bag = sum_bag / float(t)

	return sum_bag

def computeTerm5(wt,r,instanceD,inputD):
	t  = len(instanceD[r])
	p0=1

	sum_bag = 0 

	for i in instanceD[r].keys():  # i is bags , r is a randonly chosen super bag

		sum_inst = 0
		n = 0

		for j in instanceD[r][i].keys(): # j is an article in bag i

			pij = instanceD[r][i][j]
			xij = inputD[r][i][j]
			temp = getSign(pij-p0) * xij * get_oij(wt,xij,pij)
			sum_inst = sum_inst + temp
			n = n + 1

		
		sum_inst = sum_inst/float(n)
		
		sum_bag = sum_bag +  sum_inst

	sum_bag = sum_bag / float(t)

	return sum_bag


def getDeltaW(r,wt,inputD,instanceD,bagD,superbagD,Y):
	
	
	term1 = lamda * wt
	term2 = computeTerm2(r,superbagD,instanceD,inputD,Y)
	term3 = computeTerm3(r,superbagD,bagD,instanceD,inputD)
	term4 = computeTerm4(r,superbagD,bagD,instanceD,inputD)
	term5 = computeTerm5(wt,r,instanceD,inputD)
		
	delW = term1 - term2 + term3 - term4 - term5

	return delW

def computeWeight(inputD,Y,wt):
	
	eta = 0.8
	instanceD = inst_pij(wt,inputD)
	# print instanceD
	# print "****************"
	bagD = bag_Pi(instanceD)
	# print bagD
	# print "****************"
	superbagD = superbag_P(bagD)
	# print superbagD
	# print "****************"
	
	r = random.randint(1,len(superbagD))

	for r in range(1,5):
		delW = getDeltaW(r,wt, inputD, instanceD, bagD, superbagD, Y)
		wt = wt - (delW*eta)


	# print "weight: ",wt
	newInstanceD = inst_pij(wt,inputD)
	return wt, newInstanceD

	





