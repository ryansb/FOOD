
from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from time import ctime
import sys
import os
import re
restaurants = ["http://finweb.rit.edu/diningservices/brickcity",
"http://finweb.rit.edu/diningservices/commons",
"http://finweb.rit.edu/diningservices/crossroads",
"http://finweb.rit.edu/diningservices/gvcantinagrille",
"http://finweb.rit.edu/diningservices/gracies",
"http://finweb.rit.edu/diningservices/ritzsportszone"]

pretty_header = """
---------------------------------------------------
      Parser Of On-campus Preferred Specials
                      a.k.a.
        ______ ______ ______ ______  _____
       |   _  |  __  |  __  |   _  |/ ____|
       |  |_) | |  | | |  | |  |_) | (___
       |   ___| |  | | |  | |   ___|\___ \\
       |  |   | |__| | |__| |  |    ____) |
       |  |   |      |      |  |   |      |
       |__|   |______|______|__|   |_____/


     It is currently {curtime}
---------------------------------------------------
[1] Brick City Cafe
[2] Commons
[3] Crossroads
[4] Global Village Cantina and Grille
[5] Gracies
[6] Ritz Sports Zone
[q] Quit
==================================================="""

def menu():
	""" Do all the heavy lifting."""
	while True:
		# Loop till user quits.
		sel = 0
		while ( sel < 1 or sel > len(restaurants)):
			# Input validation
			print pretty_header.format(curtime=ctime())
			sel = raw_input("Enter your menu choice [1-6 or q]: ")
			if sel.lower() == "q":
				sys.exit(0)
			try:
				sel = int(sel)
			except:
				sel = 0
			os.system("clear")

		# Load meals from desired restaurant.
		html = urlopen(restaurants[sel-1])
		soup = BeautifulSoup(html, convertEntities = BeautifulSoup.HTML_ENTITIES)
		meals = soup.findAll(id=re.compile("meal_\d"))
		tabs = soup.findAll(id=re.compile("tab_\d"))

		# get the name of the restaurant, minus the "RIT Dining Services" bs.
		print ("\nOn the menu at " + re.sub("^[\w\W]*\s?:\s?", "",
			str(soup.title.string)) + " today is:")
		meal_num = 0
		for meal in meals:
			if meal:
				# print all meals served + meal name / subrestaurant name
				print ("=====================")
				print tabs[meal_num].contents[0].string
				print ("=====================\n")
				meal_num += 1
				for item in meal.findAll("li"):
					if item.string and str(item.string) != "":
						print item.string
				print ("\n")
		raw_input("Press any key to continue...")
		os.system("clear")

if sys.version[0] != "2":
	print "This script uses BeautifulSoup for html parsing."
	print "BeautifulSoup only supports Python 2.x"
menu()
