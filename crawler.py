import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from collections import OrderedDict
import pymongo
import hunspell
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["search_1"]
mycol = mydb["crawler"]

dict_1=OrderedDict([('title','doc_name')])					#for complete crawler (str to id)
dict_2=OrderedDict()
dict_3=OrderedDict()
dict_4=OrderedDict([('title','doc_id')])					#for id to str
driver=webdriver.Chrome()
wait=WebDriverWait(driver,10)
parent_url='https://en.wikinews.org'
doc_id=0
dict_3[parent_url]=[doc_id,0,0]
dict_2[doc_id]=parent_url
dict_4[str(doc_id)]=parent_url
dict_1[parent_url.replace('.','|')]=[doc_id,0,0]
ct=0
for l in dict_3:
	#print "CT", ct
	#current_url='https://www.google.co.in'
	current_url=l
	#dict_3[current_url]=[0,0]
	driver.get(current_url)
	href=set()								#for each url
	try:
		a_list=wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,'a')))
		#print "Number of anchor tags on " + current_url + "  " , len(a_list)
		for i in a_list:
			try:
				hr=i.get_attribute('href')
			except:
				pass
			else:
				if hr!=None and len(hr)!=0 and 'https://en.wiki' in hr:
					href.add(hr)
	except:					
		pass
	for i in href:
		try:
			dict_3[i][1]+=1
			dict_1[i.replace('.','|')][1]+=1
		except:
			dict_3[i]=[doc_id+1,1,0]
			dict_2[doc_id+1]=i 
			dict_4[str(doc_id+1)]=i 
			dict_1[i.replace('.','|')]=[doc_id+1,1,0]	
			doc_id+=1
	#print "Number of outgoing links on " + current_url + " " , len(href)
	dict_3[current_url][2]+=len(href)
	dict_1[current_url.replace('.','|')][2]+=len(href)
	ct+=1
	if ct==5:
		break
#print dict_2
f1=open("output.json","w")
json.dump(dict_2,f1)
print mycol.insert(dict_1)
print mycol.insert(dict_4)