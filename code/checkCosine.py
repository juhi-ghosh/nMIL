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

#getting Probability and cosine values for all articles
def getSimilar_All( targetVec , superBagsDict, newInstanceD):
	all_cos_list = []
	all_prob_list = []
	
	for k in superBagsDict.keys():
		for j in superBagsDict[k].keys():
			for i in superBagsDict[k][j].keys():

				#getting Probability density values for all articles
				all_prob_list.append(newInstanceD[k][j][i])

				#getting Cosine values for all articles
				max_score = -1.0
				for entry in targetVec:
					cos_sim = vector_cos5(superBagsDict[k][j][i], entry)
					if max_score < cos_sim:
						max_score = cos_sim
				all_cos_list.append(max_score)

	return all_cos_list, all_prob_list


#getting Probability and cosine values for all articles > tau
def getProb_Tau(targetVec_List, matrix, newInstanceD, superBagsDict):
	day_prob_list = []
	day_cos_list = []
	for inx in matrix:
		day_prob_list.append(newInstanceD[inx[0]][inx[1]][inx[2]])
		max_score=-1.0
		
		for entry in targetVec_List:
			cos_sim = vector_cos5(superBagsDict[inx[0]][inx[1]][inx[2]], entry)
			if max_score < cos_sim:
				max_score = cos_sim	
		day_cos_list.append(max_score)

	return day_prob_list, day_cos_list




#dictionary structure for instances vectors
def getSimilar_Precursors(targetVec_List,inputD,matrix):
	

	max_score = -1.0
	sel_precursor=[]
	with open('../input/dataSentences.pickle', 'rb') as handle:
		sentenceDict = pickle.load(handle)

	prevDay = matrix[0][1]
	
	day_cos_selprec_list = []

	mean_cos = 0.0
	total_cos = 0.0
	count_cos = 0
	for inx in matrix:
		print "inx:", inx, "prev:", prevDay
		max_score=-1.0
		
		for entry in targetVec_List:
			cos_sim = vector_cos5(inputD[inx[0]][inx[1]][inx[2]], entry)
			if max_score < cos_sim:
				max_score = cos_sim			
				
		if max_score>0.79:
			print "cosine_similarity", sentenceDict[inx[0]][inx[1]][inx[2]], max_score
			sel_precursor.append(sentenceDict[inx[0]][inx[1]][inx[2]])

			#creating day-wise mean list for selected cosine scores of most similar articles
			if inx[1] == prevDay:
				total_cos = total_cos + max_score
				count_cos = count_cos + 1;
			else:
				total_cos = max_score
				count_cos = 1
				
		
		if inx[1] != prevDay:
			mean_cos = total_cos/count_cos;
			print "********selected",mean_cos
			day_cos_selprec_list.append(mean_cos)
			mean_cos = 0.0
			

		#updating the day for which we calculate mean of cosine scores
		prevDay = inx[1]

	
	mean_cos = total_cos/count_cos;
	day_cos_selprec_list.append(mean_cos)

	print day_cos_selprec_list

			
	return sel_precursor, day_cos_selprec_list
	

#initialise input
superBagsDict = {}

def findCosineScore(matrix, newInstanceD):
	with open('../input/DoctoVecdata.pickle', 'rb') as handle:
			superBagsDict = pickle.load(handle)

	targetVec_List = getListTargetVec()

	sel_precursor, day_cos_selprec_list = getSimilar_Precursors(targetVec_List,superBagsDict,matrix)
	all_cos_list, all_prob_list = getSimilar_All( targetVec_List, superBagsDict, newInstanceD)
	day_prob_list, day_cos_list = getProb_Tau(targetVec_List, matrix, newInstanceD, superBagsDict)
	return (len(sel_precursor)*1.0/len(matrix)*1.0)*100, day_cos_selprec_list, all_cos_list, all_prob_list, day_prob_list,day_cos_list	


