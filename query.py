import pymongo
import re
from collections import OrderedDict
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bson.binary import Binary
import pickle
import numpy
import numpy.linalg
import hunspell
hobj = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')

def editDist(str1, str2, m, n): 
	dp = [[0 for x in range(n+1)] for x in range(m+1)] 
	for i in range(m+1): 
		for j in range(n+1): 
			if i == 0: 
				dp[i][j] = j    # Min. operations = j 
			elif j == 0: 
				dp[i][j] = i    # Min. operations = i 
			# If last characters are same, ignore last char 
			# and recur for remaining string 
			elif str1[i-1] == str2[j-1]: 
				dp[i][j] = dp[i-1][j-1] 
  
			# If last character are different, consider all 
			# possibilities and find minimum 
			else: 
				dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])     # Insert      # Remove      # Replace 
	return dp[m][n] 

stop_words=set(stopwords.words('english'))
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["search_1"]
mycol = mydb["index"]
q=mycol.find({"title":"term_name"})
for j in q:
	break
del j['_id']
del j['title']	
#print j	
m=len(j.keys())
#print m
Q=numpy.zeros((1,m))
#print Q
print "Enter Query"
query=raw_input()
print 
for q0 in query.split():
	if q0.islower():
		if q0.isalpha():
			if not hobj.spell(q0):
				li=hobj.suggest(q0)
				lis=[editDist(z,q0,len(z),len(q0)) for z in li]
				liss=[]
				for i in xrange(len(lis)):
					if lis[i]<=1:
						liss.append(li[i])
				print "Suggestions for %s "%q0,liss
r2=re.sub(r'\'[a-z]|[_0-9,();:\'\"]','',query,flags=re.IGNORECASE)
r1 = re.findall(r"[a-zA-Z\.]+[a-zA-Z]",r2)
f_list=[]
#print "r1", r1
for i in r1:
	i=i.lower()
	if i not in stop_words and '.png' not in i and '.jpg' not in i and '.jpeg' not in i and '.exe' not in i:
		f_list.append(i)
#print "flist",f_list
			
for i in f_list:
	ii=i
	#i=hobj.stem(i)
	i=i.replace('.','|')
	try:
		j[i]
	except:
		pass
	else:
		Q[0][j[i][0][0]]=1
#print Q		
mycol_0=mydb['lsi']
q=mycol_0.find()
for i in q:
	#print 1
	Ak = pickle.loads (i["key"])

print "\nFinal Result"
F=Q.dot(Ak)
FF=list(F[0])
FF_0=list(F[0])
ff=[]
for zz in xrange(len(F[0])):
	ff.append([FF[zz],zz])
ff.sort()
ff=ff[:min(10,len(ff))]
#print ff

mycol=mydb['crawler']
q=mycol.find({'title':'doc_id'})
for i in q:
	break
for j in ff:
	print i[str(j[1])]	
		