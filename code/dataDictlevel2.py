from dataDictlevel3 import instanceToVec
import os
import numpy as np

# noOfBags = len(os.listdir('./input/txtFiles'))


def bagsToVec(stBags, endBags):
	dictBags = {}

	for i in range(1,endBags-stBags+1):
		#print "bag",i
		#print "#################"
		inputFile = "../input/TextFiles/Demonitization/" + str(stBags+i-1) + ".txt"
		dictBags[i] = instanceToVec(inputFile)

	return dictBags





