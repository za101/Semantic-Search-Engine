import numpy as np 
from scipy import linalg
import pymongo
from bson.binary import Binary
import pickle


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["search_1"]
mycol = mydb["index"]
mycol_0=mydb["crawler"]
q1=mycol.find({'title':"term_id"})
for i in q1:
	m=len(i.keys())-2
q2=mycol_0.find({'title':"doc_id"})
for i in q2:
	n=len(i.keys())-2	
print "mn",m,n
#n=5
#A=np.array([ [1.0,1.0,0.0,1.0,0.0,0.0], [1.0,0.0,1.0,1.0,0.0,0.0], [1.0,1.0,1.0,2.0,1.0,1.0], [0.0,0.0,0.0,0.0,0.0,1.0]])
A=np.array([ [0.0 for i in xrange(n)] for j in xrange(m)])
#print A

q3=mycol.find({"title":"term_name"})
for i in q3:
	for z,j in i.iteritems():
		if z in ["_id","title"]:
			continue
		for k in j:
			#k[0]->term_id k[1]->doc_id k[2]->term_freq
			A[k[0]][k[1]]=k[2]
			
#print linalg.det(A)
print A

#n=6;m=4
term_freq=[sum(A[i]) for i in xrange(m)]
entropy=[]
for i in xrange(m):
	s=0
	for j in xrange(n):
		pij=A[i][j]/term_freq[i]
		if pij==0:
			continue
		s+=pij*np.log10(pij)
	s=s/(np.log10(n))
	entropy.append(s+1)
print "\nentropy\n",entropy,"\n"

A=np.array([ [entropy[i]*np.log10(A[i][j]+1) for j in xrange(n)] for i in xrange(m)])
print A
val=(Binary(pickle.dumps(A, protocol=2), subtype=128 ))
mycol = mydb["log_en"]
mycol.insert({"key":val})


