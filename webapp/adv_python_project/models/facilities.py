class Facility(object):
	def __init__(self, name, address, score):
		self._name = name
		self._address = address
		self._score = score

	def getName(self):
		return self._name

	def getAddress(self):
		return self._address

	def getScore(self):
		return self._score


class Restaurant(Facility):
	def __init__(self, name, address, score, tags, station, distance):
		super(Restaurant, self).__init__(name, address, score)
		self._tags = tags
		self._station = station
		self._distance = distance

	def getStation(self):
		return self._station

	def getDistance(self):
		return self._distance

	def getTags(self):
		return self._tags

	def asdict(self):
		return {
			'name': self._name,
			'address': self._address,
			'score': self._score,
			'station': self._station,
			'distance': self._distance,
			'tags': self._tags
		}


class Hotel(Facility):
	def __init__(self, name, address, score, star, distance):
		super(Hotel, self).__init__(name, address, score)
		self._star = star
		self._distance = distance

	def getStar(self):
		return self._star

	def getDistance(self):
		return self._distance

	def asdict(self):
		return {
			'name': self._name,
	      	'address': self._address,
	      	'score': self._score,
	      	'star': self._star,
	      	'distance': self._distance
	    }
