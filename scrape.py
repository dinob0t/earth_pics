import time
import random
import csv

import numpy as np

import Image as im

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import urllib

from nltk.tag.stanford import NERTagger
st = NERTagger('./stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz', \
'./stanford-ner-2014-06-16/stanford-ner.jar')
# print st.tag("Rami Eid is studying at Stony Brook University in NY".split())

try:
	with open('image_dict.csv', 'rb') as r: 
		reader = csv.reader(r)
		image_dict = dict(x for x in reader)
except:
	image_dict = {}

browser = webdriver.Chrome()

browser.get("http://www.reddit.com/r/earthporn")
time.sleep(2*random.random())

iterations = 1
for iteration in range(iterations):

	soup = BeautifulSoup(browser.page_source)
	links=soup.findAll('a',{'class':'title may-blank '})
	thumbs = soup.findAll('img')

	count = 0
	while count < len(links):
		cur_href = links[count]['href']
		if cur_href[0] == '/':
			links.pop(count)
		else:
			count +=1


	count = 0
	while count < len(thumbs):
		cur_thumbs_href = thumbs[count]['src']

		if cur_thumbs_href[0:3] != '//b' and cur_thumbs_href[0:3] != '//a':
			thumbs.pop(count)	
		else:
			count +=1

	thumbs = thumbs[len(thumbs) - len(links)::]

	for i in range(len(links)):
		cur_href = links[i]['href']

		cur_thumbs_href = list(thumbs[i]['src'])
		cur_thumbs_href.insert(0,'http:')
		cur_thumbs_href = ''.join(cur_thumbs_href)
		print cur_href
		print cur_thumbs_href

		success = 0
		try:
			dl = urllib.urlopen(cur_thumbs_href).read()
			success = 1

		except:
			time.sleep(1)
			dl = urllib.urlopen(cur_thumbs_href).read()
			success = 1
		finally:
			pass
		print 'successs' + str(success)
		
		f = open('tmp.jpg','wb')
		f.write(dl)
		f.close()


		cur_contents = links[i].contents
		tagger_results = st.tag(str(cur_contents).split())
		print tagger_results
		cur_image = np.asarray(im.open('tmp.jpg'))
		print cur_image.shape

	elem = browser.find_element_by_partial_link_text("next ")
	elem.send_keys(Keys.RETURN)
	time.sleep(2*random.random())

browser.quit()

time.sleep(random.random())