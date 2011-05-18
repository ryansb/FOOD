#!/usr/bin/env python

""" poops2
    python2.*
    Author: Sean Jones
    Description: My python web scraper that gets the daily dining specials of
                 restuarants on campus.
"""

from BeautifulSoup import BeautifulSoup, NavigableString
from sys import version, exit
from urllib2 import urlopen
from time import ctime


if version.split()[0] >= "3":
    print("This won't run unless you are using python version 2.*")
    exit(1)


class Restaurant(object):
    __slots__ = ("link", "contents", "undesireables", "data", "elements",
                 "new_list")

    def __init__(self, link):
        self.link = link
        self.contents = set()
        self.undesireables = set()
        self.data = dict()
        self.elements = []
        self.new_list = []
        lst = ["BUSINESS SERVICES", "Human Resources", "Digital Den", "Forms",
        "Napkin Dispenser/Table Tent Policy", "Legal Affairs", "Leadership Staff",
        "Resources", "All Day", "Information &amp; Technology Services",
        "RISK MANAGEMENT", "Bookstore", "Italian Entree",
        "Specialty Wraps-located at Deli", "Bottle Return", "Training",
        "Institute Audit, Compliance &amp; Advisement", "Weekly Menus",
        "Directories", "Facilities Management", "Parking &amp; Transportation",
        "Student Auxiliary Services", "Housing Operations", "Tiger Bucks Program",
        "Mongo's Grill", "Gordon Field House", "Hours", "Controller",
        "Mongo's", "Senior Vice President", "Student Financial Services",
        "About Us/Contacts", "Budget", "Dining Services", "In The News",
        "Special Delivery", "Global Risk Management Services",
        "Print &amp; Postal Hub", "Public Safety", "Mexican",
        "EMPLOYMENT SERVICES", "Center for Professional Development",
        "FINANCIAL SERVICES", "A-Z Index", "Nutrition", "The Works",
        "Systems &amp; Technologies", "Hot Meals Under $6",
        "Information Security", "Career Zone", "Search", "Vending",
        "Procurement Services", "Ethics &amp; Compliance",
        "Institutional Research", "Gift Cards",  "Bakery", "Veggie",
        "Meal Plans and Debit Plans", "Environmental Health &amp; Safety",
        "Locations", "Emergency Preparedness", "Business Continuity",
        "F&amp;A LEADERSHIP", "MyRIT", "F&amp;A Home", "Payroll", "Catering",
        "Tiger Bucks", "Student Employment", "Ancho",
        "RIT Inn &amp; Conference Center", "Publications", "Accounting",
        "Restaurant Vendors", "Gracies", "The Ritz Sports Zone",
        "Brick City Caf\xc3\xa9", "The Commons", "Choices",
        "The Caf\xc3\xa9 &amp; Market at the Crossroads", "Dinner", "Lunch",
        "Breakfast", "Better Me", "Same as Lunch",
        "Global Village Cantina and Grille", "Grill Special", "Bar Items",
        "Stir Fry", "Specialty Bars", "Pizza Special", "Lunch Combo Meals",
        "Soup of the Day", "Main Entree", "Deli Special", "Carb Counters",
        "Vegetarian Entree", "Chef's Special", "Soups", "Dinner Bar",
        "Lunch Grill Special", "Crossbar", "Daily Specials", "Same as Lunch",
        "Ancho Grill Rice", "Ancho Grill", "Ancho Grill Special", "Ancho Rice",
        "Just Veggie"]

        for i in lst:
            self.undesireables.add(i)

    def scrape_text(self):
        html = urlopen(self.link).read()
        soup = BeautifulSoup(html)
        self.printText(soup.findAll("li"))

    def printText(self, tags):
        for tag in tags:
            if isinstance(tag, NavigableString):
                string = str(tag)
                string = string.strip()
                if string != "":
                    if string not in self.undesireables:
                        self.contents.add(fix_string(string))
                        self.elements.append(fix_string(string))
            else:
                self.printText(tag)

    def construct_list(self):
        print "\n"
        if len(self.new_list) > 0:
            for h in self.new_list:
                print h
        elif not len(self.new_list) > 0:
            self.scrape_text()
            if len(self.contents) == 0:
                print "There doesn't appear to be anything listed here"
            else:
                for i in self.contents:
                    self.new_list.append(i)
                self.new_list.sort()
                for j in self.new_list:
                    print j
        print "\n"

brick_city_cafe = Restaurant("http://finweb.rit.edu/diningservices/brickcity")
commons = Restaurant("http://finweb.rit.edu/diningservices/commons")
crossRoads = Restaurant("http://finweb.rit.edu/diningservices/crossroads")
global_village = Restaurant(
"http://finweb.rit.edu/diningservices/gvcantinagrille")
gracies = Restaurant("http://finweb.rit.edu/diningservices/gracies")
ritz = Restaurant("http://finweb.rit.edu/diningservices/ritzsportszone")

restaurants = [brick_city_cafe, commons, crossRoads, global_village, gracies,
                ritz]


def fix_string(string):
    a = string.replace("&amp;", "&")
    b = a.replace("*", "")
    if b[0] == " ":
        b = b[1:]
    c = b.lower()
    d = c[0].upper() + c[1:]
    return d


def main():
    header = """
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

      Choose one of the following restuarants
             to view today's specials

       Today is {curtime}
---------------------------------------------------
[1] Brick City Cafe"
[2] Commons"
[3] Crossroads"
[4] Global Village Cantina and Grille"
[5] Gracies"
[6] Ritz Sports Zone"
[q] Quit"
==================================================="""
    print header.format(curtime=ctime())
    choice = raw_input("Enter your menu choice [1-6 or q]: ")
    try:
        if int(choice) >= 1 and int(choice) <= 6:
            restaurants[int(choice) - 1].construct_list()
            choice2 = raw_input("Hit the Enter key to go back to the menu, or"
                + "'q' to quit. ")
            if choice2 == "q":
                return

            else:
                main()
        else:
            print "Oops! Please select choice 1,2,3,4,5,6 or q."
            cont = raw_input("Press the Enter key to continue... ")
            while cont != "":
                cont = raw_input("Please press the Enter key... ")
            main()
    except Exception:
        if choice == 'q':
            return

        else:
            print "Oops! Please select choice 1,2,3,4,5,6 or q."
            cont = raw_input("Press the Enter key to continue... ")
            while cont != "":
                cont = raw_input("Please press the Enter key... ")
            main()

main()
