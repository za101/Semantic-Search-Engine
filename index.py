import pymongo
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from collections import OrderedDict
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import hunspell
hobj = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["search_1"]
mycol = mydb["index"]
mycol_0=mydb["crawler"]
url_list=[]
t1=mycol_0.find({'title':"doc_id"})
for i in t1:
	maxi=float("-inf")
	for j in i.keys():
		try:
			x=int(j)
		except:
			pass
		else:
			if x>maxi:
				maxi=x
	for j in xrange(maxi+1):
		url_list.append(i[str(j)])
#print len(url_list)
#print url_list			
					

dict_1=OrderedDict([("title","term_name")])					#for complete crawler
dict_2=OrderedDict([("title","term_id")])
term_id=0
driver=webdriver.Chrome()
wait=WebDriverWait(driver,10)
stop_words=set(stopwords.words('english'))
punctuations=[',',";","'",'"','.',':',')','(']
doc_id=0
#url_list=['https://en.wikipedia.org/wiki/Web_search_engine','https://www.geeksforgeeks.org/search-engines-work/','https://www.geeksforgeeks.org/understanding-search-engines/',
#'https://en.wikipedia.org/wiki/Search_engine_indexing','https://www.techopedia.com/definition/12708/search-engine-world-wide-web']
for current_url in url_list:
	driver.get(current_url)
	try:
		driver.find_element_by_xpath(' //*[@id="siteNotice"]/div[2]/div[1]/a').click()
	except:
		pass	
	body_content=wait.until(EC.presence_of_element_located((By.TAG_NAME,'body')))
	#content_list=body_content.text[:50].strip().split()
	#s=set(content_list)
	#for i in content_list:
	#	for j in punctuations:
	xx=body_content.text[:100]
	r2=re.sub(r'\'[a-z]|[_0-9,();:\'\"]','',xx,flags=re.IGNORECASE)
	#print r2
	r1 = re.findall(r"[a-zA-Z\.]+[a-zA-Z]",r2)
	f_list=[]
	print "r1", r1
	for i in r1:
		i=i.lower()
		if i not in stop_words and '.png' not in i and '.jpg' not in i and '.jpeg' not in i and '.exe' not in i:
			f_list.append(i)
	print "flist",f_list
			
	for i in f_list:
		ii=i
		#i=hobj.stem(i)
		i=i.replace('.','|')
		try:
			dict_1[i]
		except:
			dict_1[i]=[[term_id,doc_id,1]]
			dict_2[str(term_id)]=ii
			term_id+=1
		else:
			if dict_1[i][-1][1]==doc_id:
				dict_1[i][-1][2]+=1
			else:
				dict_1[i].append([dict_1[i][-1][0],doc_id,1])	

	#for i in s:
	#	for j in punctuations:
	#		i=i.strip(j)
	#	i=i.lower()
	#	i=i.rstrip("'s")				#remove integer as well
	#	if i in stop_words:
	#		continue					#removing stopwords after converting to lower case
	#	try:
	#		dict_1[i].append(current_url)
	#	except:
	#		dict_1[i]=[current_url]
	#for key,value in dict_1.items():
	#	print key,value		
	doc_id+=1	
	if doc_id==100:
		break		
f1=open("output_index.json","w")
json.dump(dict_2,f1)
x=mycol.insert(dict_1)
print x
mycol.insert(dict_2)

'''
import re
xx = "guru't99 egducabation. i.s. f.u.n."
r2=re.sub(r'\'[a-z]|[0-9,();:\'\"]','',xx,flags=re.IGNORECASE)
print r2
r1 = re.findall(r"[a-zA-z\.]+[a-zA-Z]",r2)
print r1
'''