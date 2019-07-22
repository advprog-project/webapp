# -*- coding: utf-8 -*-
import os
# from io import open

import jinja2
import webapp2

from models.facilities import Restaurant

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class RestaurantPage(webapp2.RequestHandler):

	def __init__(self, *args, **kwargs):
		# Due to python2
		super(RestaurantPage, self).__init__(*args, **kwargs)
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
				name = items[1].decode('utf-8')
				address = items[2].decode('utf-8')
				score = float(items[3])
				tags = (items[4].replace("??", "/")).strip().split('、')
				tags = [tag.decode('utf-8') for tag in tags]
				stationDistance = items[5].split(" ")
				station = stationDistance[0].decode('utf-8')
				distance = int(stationDistance[1].rstrip("m"))
				restaurant = Restaurant(name, address, score, tags, station, distance)
				restaurants.append(restaurant)
			fileHandler.close()
			return restaurants
		except IOError:
			print("Error: restaurant.csv does not exist or it can't be opened.")
			
	def readHotels(file_path):
	 	try:
		    hotels = []
		    fileHandler = open(file_path)
		    lines = fileHandler.readlines()
		    for i in range(1, len(lines)):
			      line = lines[i]
			      items = line.strip().split(',')
			      name = items[1].decode('utf-8')
			      address1 = items[2].decode('utf-8')
			      address2 = items[3].decode('utf-8')
			      score = float(items[4])
			      # TODO utf-8
			      star = int(items[5])
			      stationDistance = items[6].split(" ")
			      distance = float(stationDistance[1].rstrip("km"))
			      address = address1 + address2
			      hotel = Hotel(name, address, score, star, distance)
			      print(hotel.name, hotel.address, hotel.score, hotel.star, hotel.distance)
			      hotels.append(hotel)
		    fileHandler.close()
		    return hotels
		except IOError:
			print("Error: hotel.csvs does not exist or it can't be opened.")
	
	
	
	def get(self):
		print(self.request.query_string)
		restaurants = list(map(lambda x: x.asdict(), self.__restaurants))

		template_values = {
			'restaurants': restaurants[0:self.__recordLimit]
		}
		print(restaurants[0])

		template = JINJA_ENVIRONMENT.get_template('restaurants.html')
		self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
		self.response.write(template.render(template_values))

	def post(self):
		# tyuka = self.request.get('tyuka', 'restaurants')
		# print(tyuka)
		pass


class HotelPage(webapp2.RequestHandler):

	def __init__(self, *args, **kwargs):
		# Due to python2
		super(HotelPage, self).__init__(*args, **kwargs)
		self.__hotels = self.readHotels("data/restaurant.csv")
		self.__recordLimit = 5

	""" exception
        readfile 
        thread: read two files in two threads"""
	def readHotels(self, file_path):
		try:
			restaurants = []
			fileHandler = open(file_path)
			lines = fileHandler.readlines()
			for i in range(1, len(lines)):
				line = lines[i]
				items = line.strip().split(',')
				name = items[1].decode('utf-8')
				address = items[2].decode('utf-8')
				score = float(items[3])
				tags = (items[4].replace("??", "/")).strip().split('、')
				tags = [tag.decode('utf-8') for tag in tags]
				stationDistance = items[5].split(" ")
				station = stationDistance[0].decode('utf-8')
				distance = int(stationDistance[1].rstrip("m"))
				restaurant = Restaurant(name, address, score, tags, station, distance)
				restaurants.append(restaurant)
			fileHandler.close()
			return restaurants
		except IOError:
			print("Error: restaurant.csv does not exist or it can't be opened.")

	def get(self):
		hotels = list(map(lambda x: x.asdict(), self.__hotels))

		template_values = {
			'restaurants': hotels[0:self.__recordLimit]
		}

		template = JINJA_ENVIRONMENT.get_template('hotels.html')
		self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
		self.response.write(template.render(template_values))

	def post(self):
		pass


class MainPage(webapp2.RequestHandler):

	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
		self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/restaurants', RestaurantPage),
	('/hotels', HotelPage)
], debug=True)
