import pickle
#from sklearn.metrics.pairwise import cosine_similarity
import gensim.models as g
import codecs
import numpy as np
import math

def vector_cos5(v1, v2):
    
   v1 = np.array(v1)
   v2 = np.array(v2)
   prod = np.dot(v1, v2)
   len1 = math.sqrt(np.dot(v1, v1))
   len2 = math.sqrt(np.dot(v2, v2))
   return prod / (len1 * len2)*1.0

def getListTargetVec():
	#python example to infer document vectors from trained doc2vec model
	#parameters
	model="../input/model/model.bin"
	test_docs="../input/model/test2.txt"

	#inference hyper-parameters
	start_alpha=0.01
	infer_epoch=1000

	#load model
	m = g.Doc2Vec.load(model)
	test_docs = [ x.strip().split() for x in codecs.open(test_docs, "r", "utf-8").readlines() ]

	#infer test vectors
	l = []
	targetInstances = []
	for d in test_docs:
	    l= [float(x) for x in m.infer_vector(d, alpha=start_alpha, steps=infer_epoch)]
	    targetInstances.append(np.array(l))

	return targetInstances  


#dictionary structure for instances vectors
def getSimilar_Precursors(targetVec_List,inputD,matrix):

	max_score = -1.0
        sel_precursor=[]
        with open('../input/dataSentences.pickle', 'rb') as handle:
  		sentenceDict = pickle.load(handle)

	for inx in matrix:
		max_score=-1.0
		for entry in targetVec_List:
			cos_sim = vector_cos5(inputD[inx[0]][inx[1]][inx[2]], entry)
			if max_score < cos_sim:
				max_score = cos_sim
				
		if max_score>0.75:
			print "cosine_similarity", sentenceDict[inx[0]][inx[1]][inx[2]], max_score
			sel_precursor.append(entry)
			
	
	return sel_precursor
	

#initialise input
superBagsDict = {}
targetVec = {}
def findCosineScore(matrix):
	with open('../input/DoctoVecdata.pickle', 'rb') as handle:
	  		superBagsDict = pickle.load(handle)

	targetVec_List = getListTargetVec()
	sel_precursor = getSimilar_Precursors(targetVec_List,superBagsDict,matrix)
	return (len(sel_precursor)*1.0/len(matrix)*1.0)*100	


