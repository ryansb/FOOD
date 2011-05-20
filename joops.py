"""
Author: Sam Lucidi
"""
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString
from urllib2 import urlopen
import re
import json
import sys

restaurants = ["http://finweb.rit.edu/diningservices/brickcity",
"http://finweb.rit.edu/diningservices/commons",
"http://finweb.rit.edu/diningservices/crossroads",
"http://finweb.rit.edu/diningservices/gvcantinagrille",
"http://finweb.rit.edu/diningservices/gracies",
"http://finweb.rit.edu/diningservices/ritzsportszone"]


def services():
	dict_blob = {"services": []}
	for serv in restaurants:
		dict_blob["services"].append(get_menu_dict(serv))
	return json.dumps(dict_blob)


def get_menu_dict(url):
	""" Returns a RIT Dining Services
	menu as a convenient json blob. """
	html = urlopen(url)
	soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
	meals = soup.findAll(id=re.compile("meal_\d"))
	tabs = soup.findAll(id=re.compile("tab_\d"))
	# get the name of the restaurant, minus the "RIT Dining Services" bs.
	dict_blob = {"restaurant": re.sub("^[\w\W]*\s?:\s?", "",
		soup.title.string).encode('utf-8')}
	meal_num = 0
	for meal in meals:
		if meal:
			dict_blob[tabs[meal_num].contents[0].string] = []
			for item in meal.findAll("li"):
				if item.string and str(item.string) != "":
					dict_blob[
					tabs[meal_num].contents[0].string
					].append(unicode(item.string).encode('utf-8'))
			meal_num += 1
	return dict_blob

if __name__ == '__main__':
	print services()
