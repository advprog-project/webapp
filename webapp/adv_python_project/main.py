# -*- coding: utf-8 -*-
import os
from urllib import unquote
import operator
from collections import defaultdict

import jinja2
import webapp2

from models.facilities import Restaurant

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class FacilityPage(webapp2.RequestHandler):
	pass


class RestaurantPage(webapp2.RequestHandler):

	def __init__(self, *args, **kwargs):
		# Due to python2
		super(RestaurantPage, self).__init__(*args, **kwargs)
		self.__restaurants = self.readRestaurants("data/restaurant.csv")
		self.__recordLimit = 5
		self.__tagMap = {
			'tyuuka': u'中華料理', # need to add 'u' in front to convert to unicode
			'izakaya': u'居酒屋',
			'tukemen': u'つけ麺'
		}
		self.__stationMap = {
			'toden': u'早稲田（都電）駅',
			'omokage': u'面影橋駅',
			'waseda': u'早稲田（メトロ）駅',
			'takadanobaba': u'高田馬場駅',
			'nishiwaseda': u'西早稲田駅'
		}

	def queryParser(self, query):
		items = query.split('&') if query != '' else []
		keyMap = defaultdict(str)
		for item in items:
			k, v = item.split('=')
			keyMap[k] = v

		distance = keyMap['distance']
		keyword = keyMap['keyword']
		keyword = unquote(keyword).decode('utf8')
		sortBy = keyMap['sortBy']
		sortOrder = keyMap['sortOrder']
		station = keyMap['station']

		try:
			distance = float(distance) if distance != "" else float('inf')
		except ValueError:
			# TODO handle exception
			distance = float('inf')

		# except NegativeDistanceError:

		tags = []
		for k, v in keyMap.items():
			if v == '1':
				tags.append(k)

		return {
			'keyword': keyword,
			'distance': distance,
			'tags': tags,
			'sortBy': sortBy,
			'sortOrder': sortOrder,
			'station': station
		}

	def filterRestaurants(self, query):  # dictionary
		keyWordFilter = query['keyword']
		distanceFilter = query['distance']
		tagsFilter = query['tags']
		stationFilter = query['station']
		tagsNumber = len(tagsFilter)
		filteredRestaurants = []
		# A list containing all the keywords (no longer a string due to the (possibly) space in user input)
		wordsFilter = keyWordFilter.split()
		for restaurant in self.__restaurants:
			hasSmallerDistance = False
			containsKeyword = False
			containsTag = False
			containsStation = False
			tagDet = 0
			# check distance range
			if restaurant.getDistance() <= distanceFilter:
				hasSmallerDistance = True

			# check keywords
			if len(wordsFilter) == 0:
				containsKeyword = True
			else:
				for word in wordsFilter:
					if word in restaurant.getName():
						containsKeyword = True
						break

			# check tags
			for tagFilter in tagsFilter:  # tag of user input
				for tag in restaurant.getTags():  # tag of restaurant
					if self.__tagMap[tagFilter] == tag:
						tagDet += 1
			if (tagDet == tagsNumber) or tagsNumber == 0:  # contains all the user input tags
				containsTag = True

			# check stations
			if (stationFilter == '') or restaurant.getStation() == self.__stationMap[stationFilter]:  # contains user input station
				containsStation = True

			# satisfy all the three requirements
			if hasSmallerDistance and containsKeyword and containsTag and containsStation:
				filteredRestaurants.append(restaurant)

		return filteredRestaurants

	# sort method can be used for facility class
	def sortRestaurants(self, restaurants, query):  # sortOrder = sortBy[1]
		sortOrder = query['sortOrder']
		sortBy = query['sortBy']
		if sortOrder == '' or sortBy == '':
			return restaurants

		reverse = None
		if sortOrder == 'asc':
			reverse = False
		elif sortOrder == 'des':
			reverse = True
		else:
			# exception
			pass

		if sortBy == 'score':
			restaurants.sort(key=lambda x: x.getScore(), reverse=reverse)
		elif sortBy == 'distance':
			restaurants.sort(key=lambda x: x.getDistance(), reverse=reverse)
		else:
			# exception
			pass
		return restaurants

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

	def get(self):
		query = self.request.query_string
		query = self.queryParser(query)
		restaurants = self.filterRestaurants(query)
		restaurants = self.sortRestaurants(restaurants, query)
		restaurants = list(map(lambda x: x.asdict(), restaurants))


		template_values = {
			'restaurants': restaurants[0:self.__recordLimit]
		}

		template = JINJA_ENVIRONMENT.get_template('restaurants.html')
		self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
		self.response.write(template.render(template_values))


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