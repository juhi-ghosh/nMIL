#python example to infer document vectors from trained doc2vec model
import gensim.models as g
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np

def instanceToVec(inputFile):
	#parameters
	
	test_docs=inputFile

	#inference hyper-parameters
	start_alpha=0.01
	infer_epoch=1000

	#load model
	# m = g.Doc2Vec.load(model)
	test_docs = [ x.strip().split() for x in codecs.open(test_docs, "r", "utf-8").readlines() ]

	#infer test vectors
	l = []
	dictInstances = {}
	i = 1
	for d in test_docs:
		
		s = " ".join(d)
		#print s
		dictInstances[i] = s
		i = i+1
	print dictInstances

	return dictInstances
