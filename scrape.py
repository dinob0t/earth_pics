import time
import random
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import urllib2

from nltk.tag.stanford import NERTagger
st = NERTagger('./stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz', \
'./stanford-ner-2014-06-16/stanford-ner.jar')
print st.tag("Rami Eid is studying at Stony Brook University in NY".split())

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
	for link in links:
		cur_href = link['href']
		if cur_href[0] != '/':
			cur_contents = link.contents
			tagger_results = st.tag(str(cur_contents).split())
			print tagger_results


	elem = browser.find_element_by_partial_link_text("next ")
	elem.send_keys(Keys.RETURN)
	time.sleep(2*random.random())

browser.quit()

time.sleep(random.random())