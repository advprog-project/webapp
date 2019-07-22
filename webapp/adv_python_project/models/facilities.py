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
		return self.__name + self.__address + str(self.__score) + self.__station + str(self.__distance)

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
				
class Hotel(Facility):
	def __init__(self, name, address, score, star):
		Facility.__init__(self, name, address, score, NW_distance)
		self.star = star
		self.NW_distance = NW_distance
	def __str__(self):
		return self.__name + self.__address + str(self.__score) + str(self.__NW_distance)

	def getDistance(self):
		return self.__NW_distance

	def asdict(self):
		return {
			'name': self.__name,
			'address': self.__address,
			'score': self.__score,
			'star': self.__star
			'distance': self.__NW_distance
		}	
