from dataDictlevel2 import bagsToVec
import os
import numpy as np
import pickle



dictSuperBags = {}

noOfBags = len(os.listdir('../input/TextFiles/Demonitization'))
t = 5
noOfSuperBags = noOfBags / t

cnt = 1
for i in range(1,noOfSuperBags+1):
	# print "super",i
	# print "*******************************************"
	dictSuperBags[i] = bagsToVec(cnt,cnt+t)
	print dictSuperBags[i].keys()
	cnt = cnt+t

with open('../input/dataSentences.pickle', 'wb') as handle:
		pickle.dump(dictSuperBags, handle)


