# -*- coding: utf-8 -*-  
import urllib
import urllib2 
import cookielib
import os
import time
import re
from HTMLParser import HTMLParser
import sys

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links =  []
	def handle_starttag(self, tag, attrs):
#		print "Encountered the beginning of a %s tag" % tag
		if tag == 'img' or tag == "script":
			for (variable, value)  in attrs:
				if variable == "src" or variable == "href":
					self.links.append(value)
		if tag == "link":
			dic = dict(attrs)
			if dic['rel']=="stylesheet":
				self.links.append(dic['href'])

def get_file(url):
    try:
	cj=cookielib.LWPCookieJar()
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)               
	req=urllib2.Request(url)
	operate=opener.open(req)
	data=operate.read()
	return data
    except BaseException, e:
	print e
	return None

def backup(data,i,links):
    if i < 10:
           i_string = '000%d' %i
    elif i<100:
           i_string = '00%d' %i
    else:
           i_string = '0%d' %i 
	   
    tmp_path = os.getcwd() + '\\tmp\\backup\\20150630' + i_string
    isExists = os.path.exists(tmp_path)
    if not isExists:
        print tmp_path + '创建成功'
        os.makedirs(tmp_path)
    else:
        os.chdir(tmp_path) 
    file_object = open(tmp_path+'\\index.html','w')
    file_object.write(data)
    file_object.close()
    
    for link in links:
	if link[-3:] == 'jpg' or link[-3:] =='png':
		img_name = link.rsplit('/')[-1]
		tmp_path_img = tmp_path + '\\images'
		if os.path.exists(tmp_path_img) is False:
				os.mkdir(tmp_path_img) 		
		urllib.urlretrieve(link,tmp_path_img +'\\'+ img_name)
		
	if link[-3:] == 'css':
		css_name = link.rsplit('/')[-1]
		tmp_path_css = tmp_path + '\\css'
		if os.path.exists(tmp_path_css) is False:
			os.mkdir(tmp_path_css)  		
		urllib.urlretrieve(link,tmp_path_css +'\\'+ css_name)
		
	if link[-2:] == 'js':
		js_name = link.rsplit('/')[-1]
		tmp_path_js = tmp_path + '\\js'
		if os.path.exists(tmp_path_js) is False:
			os.mkdir(tmp_path_js)  		
		urllib.urlretrieve(link,tmp_path_js +'\\'+ js_name)               
if __name__ == '__main__':
	url='http://m.sohu.com'
	data = get_file(url) 
	hp = MyHTMLParser()
	hp.feed(data)	
	i = 1
	while True:
	      backup(data,i,list(set(hp.links)))
	      time.sleep(60)
	      i+=1
	      if i >= 1000:
		 i = 1  

    
