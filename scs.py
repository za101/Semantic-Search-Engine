from bson.binary import Binary
import pickle
import numpy
import numpy.linalg
import pymongo
#numpy.set_printoptions(formatter= {"float": lambda x: ("%.2f" % x)})
#A=numpy.zeros((4,6))


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["search_1"]
mycol = mydb["log_en"]
#mycol.insert({"key":val})
q=mycol.find()
for i in q:
	#print 1
	A = pickle.loads (i["key"])
m=len(A)	
n=len(A[0])

#print A
'''
Term						documents								query  web surfing   0  1  1  0
			d1		d2		d3		d4		d5		d6
internet	1		1		0		1		0		0
web			1		0		1		1		0		0
surfing		1		1		1		2		1		1
beach      	0		0		0		1		1		1

'''

#A[0][0]=A[0][1]=A[0][3]=A[1][0]=A[1][2]=A[1][3]=A[2][0]=A[2][1]=A[2][2]=A[2][4]=A[2][5]=A[3][3]=A[3][4]=A[3][5]=1
#A[2][3]=2
print "Term doc matrix\n",A,"\n"
print 
#query = numpy.array([0,1,1,0])
#print "query * A\n",query.dot(A)
#print 

[U,S,V] = numpy.linalg.svd(A)
#print U
#print S
#print V
d=len(S)
U = U[:m,:d]
S = numpy.diag(S)
V = V[:d,:n]
print "\nSVD decomposition of A\n"
print U
print len(U),len(U[0])
print 
print S
print len(S),len(S[0])
print
print V
print len(V),len(V[0])
print 

k=50 #topic chosen

U = U[:,:k]
S = S[:k,:k]
V = V[:k,:]

Ak = U.dot(S).dot(V)
print "Approximation of term doc matrix\n"
print Ak
print 
val=(Binary(pickle.dumps(Ak, protocol=2), subtype=128 ) )
mycol = mydb["lsi"]
#print S[50][50]
mycol.insert({"key":val})


#print "query * A\n",query.dot(Ak)
#print 


'''
print "Verifying U*S*V=A"
print U.dot(S).dot(V)
print "Verifying U*S*V=A"
print U.dot(S).dot(V)
print 
print "U is column orthonormal matrix"
print U.transpose().dot(U)
print
print "V is row orthogonal matrix"
print V.dot(V.transpose())
print
'''
'''
from bson.binary import Binary
import pickle
import numpy
A=numpy.zeros((4,6))
val=(Binary(pickle.dumps(A, protocol=2), subtype=128 ) )
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["search_1"]
mycol = mydb["ngram"]
mycol.insert({"key":val})
q=mycol.find()
for i in q:
	print 1
	print pickle.loads (i["key"])
'''
