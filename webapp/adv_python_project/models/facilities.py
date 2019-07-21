class Facility:
	def __init__(self, name, address, score):
		self.__name = name 
		self.__address = address
		self.__score = score

	def getName(self):
		return self.__name

	def getAddress(self):
		return self.__address

	def getScore(self):
		return self.__score


class Restaurant(Facility):
	def __init__(self, name, address, score, tags, station, distance):
		Facility.__init__(self, name, address, score)
		self.__tags = tags
		self.__station = station
		self.__distance = distance

	def __str__(self):
		return self.name + self.address + str(self.score) + self.station + str(self.distance)

	def getStation(self):
		return self.__station

	def getDistance(self):
		return self.__distance

	def asdict(self):
		return {
			'name': self.__name,
			'address': self.__address,
			'score': self.__score,
			'station': self.__station,
			'distance': self.__distance
		}
				
# class Hotel(Facility):
# 	def __init__(self, name, address, score, star):
# 		Facility.__init__(self, name, address, score)
# 		self.star = star