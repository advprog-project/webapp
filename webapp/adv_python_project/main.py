# -*- coding: utf-8 -*-
import os
from urllib import unquote
import operator
from collections import defaultdict

import jinja2
import webapp2

from models.facilities import Restaurant, Hotel
from custom_exceptions.exceptions import NegativeDistanceError

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class FacilityPage(webapp2.RequestHandler):

	def __init__(self, *args, **kwargs):
		csvPath = kwargs["csvPath"]
		del kwargs["csvPath"]
		super(FacilityPage, self).__init__(*args, **kwargs)
		self._facilities = self.readFacilities(csvPath)
		self._recordLimit = 5

	def readFacilities(self, csvPath):
		raise NotImplementedError

	def parseQuery(self, query):
		raise NotImplementedError

	def filterFacilities(self, facilities, query):
		raise NotImplementedError

	def sortFacilities(self, facilities, query):
		raise NotImplementedError

	def get(self):
		raise NotImplementedError


class RestaurantPage(FacilityPage):

	def __init__(self, *args, **kwargs):
		# Need to call super() like this due to python 2
		kwargs["csvPath"] = "data/restaurant.csv"
		super(RestaurantPage, self).__init__(*args, **kwargs)
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

	def readFacilities(self, csvPath):
		try:
			restaurants = []
			fileHandler = open(csvPath)
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

	def parseQuery(self, query):
		items = query.split('&') if query != '' else []
		keyMap = defaultdict(str)
		for item in items:
			k, v = item.split('=')
			keyMap[k] = v

		distance = keyMap['dist']
		keyword = keyMap['keyword']
		keyword = unquote(keyword).decode('utf8')
		sortBy = keyMap['sortBy']
		sortOrder = keyMap['sortOrder']
		station = keyMap['station']

		try:
			distance = float(distance) if distance != "" else float('inf')
		except ValueError:
			raise ValueError('Distance should be a numeric value.')
		if distance < 0:
			raise NegativeDistanceError('Distance should be non-negative.')

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

	def filterFacilities(self, restaurants, query):  # dictionary
		keyWordFilter = query['keyword']
		distanceFilter = query['distance']
		tagsFilter = query['tags']
		stationFilter = query['station']
		tagsNumber = len(tagsFilter)
		filteredRestaurants = []
		# A list containing all the keywords (no longer a string due to the (possibly) space in user input)
		wordsFilter = keyWordFilter.split()
		for restaurant in restaurants:
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
	def sortFacilities(self, restaurants, query):  # sortOrder = sortBy[1]
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
			raise

		if sortBy == 'score':
			restaurants.sort(key=lambda x: x.getScore(), reverse=reverse)
		elif sortBy == 'distance':
			restaurants.sort(key=lambda x: x.getDistance(), reverse=reverse)
		return restaurants

	def get(self):
		query = self.request.query_string
		restaurants = self._facilities
		template_values = {}
		errorMessage = ''
		try:
			query = self.parseQuery(query)
			restaurants = self.filterFacilities(restaurants, query)
			restaurants = self.sortFacilities(restaurants, query)
		except ValueError as e:
			errorMessage = str(e)
		except NegativeDistanceError as e:
			errorMessage = str(e)
		except Exception as e:
			errorMessage = str(e)
		restaurants = list(map(lambda x: x.asdict(), restaurants))
		template_values['restaurants'] = restaurants[0:self._recordLimit]
		template_values['error'] = errorMessage
		template = JINJA_ENVIRONMENT.get_template('restaurants.html')
		self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
		self.response.write(template.render(template_values))


class HotelPage(FacilityPage):

	def __init__(self, *args, **kwargs):
		kwargs["csvPath"] = "data/hotel.csv"
		super(HotelPage, self).__init__(*args, **kwargs)
			
	def readFacilities(self, csvPath):
		try:
			hotels = []
			fileHandler = open(csvPath)
			lines = fileHandler.readlines()
			for i in range(1, len(lines)):
				line = lines[i]
				items = line.strip().split(',')
				name = items[1].decode('utf-8')
				address1 = items[2].decode('utf-8')
				address2 = items[3].decode('utf-8')
				score = float(items[4])
				star = int(items[5])
				stationDistance = items[6].split(" ")
				station = stationDistance[0].decode('utf-8')
				distance = int(float(stationDistance[1].rstrip("km")) * 1000)
				address = address1 + address2
				hotel = Hotel(name, address, score, star, station, distance)
				hotels.append(hotel)
			fileHandler.close()
			return hotels
		except IOError:
			print("Error: hotel.csv does not exist or it can't be opened.")

	def parseQuery(self, query):
		items = query.split('&') if query != '' else []
		keyMap = defaultdict(str)
		for item in items:
			k, v = item.split('=')
			keyMap[k] = v

		distance = keyMap['dist']
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

		stars = []
		for k, v in keyMap.items():
			if v == '1':
				stars.append(int(k))

		return {
			'keyword': keyword,
			'distance': distance,
			'stars': stars,
			'sortBy': sortBy,
			'sortOrder': sortOrder,
			'station': station
		}

	def filterFacilities(self, hotels, query):  # dictionary
		keyWordFilter = query['keyword']
		distanceFilter = query['distance']
		starsFilter = query['stars']
		stationFilter = query['station']
		starsNumber = len(starsFilter)
		filteredHotels = []
		# A list containing all the keywords (no longer a string due to the (possibly) space in user input)
		wordsFilter = keyWordFilter.split()
		for hotel in hotels:
			hasSmallerDistance = False
			containsKeyword = False
			containsStar = False
			containsStation = False
			starDet = 0
			# check distance range
			if hotel.getDistance() <= distanceFilter:
				hasSmallerDistance = True

			# check keywords
			if len(wordsFilter) == 0:
				containsKeyword = True
			else:
				for word in wordsFilter:
					if word in hotel.getName():
						containsKeyword = True
						break

			# check tags
			if len(starsFilter) == 0:
				containsStar = True
			else:
				for starFilter in starsFilter:  # star of user input
					if hotel.getStar() == starFilter:
						containsStar = True
			# check stations
			if (stationFilter == '') or hotel.getStation() == self.__stationMap[stationFilter]:  # contains user input station
				containsStation = True

			# satisfy all the three requirements
			if hasSmallerDistance and containsKeyword and containsStar and containsStation:
				filteredHotels.append(hotel)

		return filteredHotels

	# sort method can be used for facility class
	def sortFacilities(self, hotels, query):  # sortOrder = sortBy[1]
		sortOrder = query['sortOrder']
		sortBy = query['sortBy']
		if sortOrder == '' or sortBy == '':
			return hotels

		reverse = None
		if sortOrder == 'asc':
			reverse = False
		elif sortOrder == 'des':
			reverse = True
		else:
			# exception
			pass

		if sortBy == 'score':
			hotels.sort(key=lambda x: x.getScore(), reverse=reverse)
		elif sortBy == 'distance':
			hotels.sort(key=lambda x: x.getDistance(), reverse=reverse)
		else:
			# exception
			pass
		return hotels

	def get(self):
		query = self.request.query_string
		query = self.parseQuery(query)
		hotels = self._facilities
		hotels = self.filterFacilities(hotels, query)
		hotels = self.sortFacilities(hotels, query)
		hotels = list(map(lambda x: x.asdict(), hotels))

		template_values = {
			'hotels': hotels[0:self._recordLimit]
		}

		template = JINJA_ENVIRONMENT.get_template('hotels.html')
		self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
		self.response.write(template.render(template_values))


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
