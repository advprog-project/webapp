class Facility(object):
	"""
	Main author: ZHOU yanjun
	"""
	def __init__(self, name, address, score, station, distance):
		self._name = name
		self._address = address
		self._score = score
		self._station = station
		self._distance = distance

	def getName(self):
		return self._name

	def getAddress(self):
		return self._address

	def getScore(self):
		return self._score

	def getStation(self):
		return self._station

	def getDistance(self):
		return self._distance


class Restaurant(Facility):
	"""
	authors: ZHOU Yanjun, HU Yuxin
	"""
	def __init__(self, name, address, score, tags, station, distance):
		super(Restaurant, self).__init__(name, address, score, station, distance)
		self._tags = tags

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
	"""
	authors: ZHOU Yanjun, HU Yuxin
	"""
	def __init__(self, name, address, score, star, station, distance):
		super(Hotel, self).__init__(name, address, score, station, distance)
		self._star = star

	def getStar(self):
		return self._star

	def asdict(self):
		return {
			'name': self._name,
			'address': self._address,
			'score': self._score,
			'star': self._star,
			'station': self._station,
			'distance': self._distance,
		}
