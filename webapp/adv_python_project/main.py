# -*- coding: utf-8 -*-
import os
import urllib

import jinja2
import webapp2

from models import Restaurant

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

	def __init__(self):
		self.__restaurants = self.readRestaurants("restaurant.csv")
		self.__recordLimit = 5

	""" exception
        readfile 
        thread: read two files in two threads"""
	def readRestaurants(self, file_path):
		try:
			restaurants = []
			lines = open(file_path)
			lines.readline()
			for line in lines:
				items = line.strip().split(',')
				name = items[1]
				address = items[2]
				score = items[3]
				tags = (items[4].replace("??", "/")).strip().split('、')
				stationDistance = items[5].split(" ")
				station = stationDistance[0]
				distance = int(stationDistance[1].rstrip("m"))
				restaurant = Restaurant(name, address, score, tags, station, distance)
				restaurants.append(restaurant)
			lines.close()
			return restaurants
		except IOError:
			print("Error: restaurant.csv does not exist or it can't be opened.")


	def get(self):
		template_values = {
			'restaurants': self.restaurants[0:self.__recordLimit]
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)