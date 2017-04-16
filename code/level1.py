from level2 import bagsToVec
import os
import numpy as np
import pickle



dictSuperBags = {}

noOfBags = len(os.listdir('../input/TextFiles/Demonitization'))
t = 5
noOfSuperBags = noOfBags / t

cnt = 1
for i in range(1,noOfSuperBags+1):
	print "super",i
	# print "*******************************************"
	dictSuperBags[i] = bagsToVec(cnt,cnt+t)
	print dictSuperBags[i].keys()
	cnt = cnt+t

with open('../input/DoctoVecdata.pickle', 'wb') as handle:
		pickle.dump(dictSuperBags, handle)


print dictSuperBags[1].keys()
print dictSuperBags[2].keys()
print len(dictSuperBags)


