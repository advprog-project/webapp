# -*- coding: utf-8 -*-
import os
import urllib

import jinja2
import webapp2

from models.facilities import Restaurant

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

	def __init__(self, *args, **kwargs):
		# Due to python2
		super(MainPage, self).__init__(*args, **kwargs)
		self.__restaurants = self.readRestaurants("data/restaurant.csv")
		self.__recordLimit = 5

	""" exception
        readfile 
        thread: read two files in two threads"""
	def readRestaurants(self, file_path):
		try:
			restaurants = []
			fileHandler = open(file_path)
			lines = fileHandler.readlines()
			for i in range(1, len(lines)):
				line = lines[i]
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
			fileHandler.close()
			return restaurants
		except IOError:
			print("Error: restaurant.csv does not exist or it can't be opened.")


	def get(self):
		print(self.__restaurants)
		template_values = {
			'restaurants': self.__restaurants[0:self.__recordLimit]
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)