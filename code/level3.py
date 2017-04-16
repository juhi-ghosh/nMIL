#python example to infer document vectors from trained doc2vec model
import gensim.models as g
import codecs
import numpy as np

def instanceToVec(inputFile):
	#parameters
	model="../input/model/model.bin"
	test_docs=inputFile

	#inference hyper-parameters
	start_alpha=0.01
	infer_epoch=1000

	#load model
	m = g.Doc2Vec.load(model)
	test_docs = [ x.strip().split() for x in codecs.open(test_docs, "r", "utf-8").readlines() ]

	#infer test vectors
	l = []
	dictInstances = {}
	i = 1
	for d in test_docs:
	    l= [float(x) for x in m.infer_vector(d, alpha=start_alpha, steps=infer_epoch)]
	    dictInstances[i] = np.array(l)
	    i = i+1

	return dictInstances
