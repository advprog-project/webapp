class Facility(object):
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
		super(Restaurant, self).__init__(name, address, score)
		self.__tags = tags
		self.__station = station
		self.__distance = distance

	# def __str__(self):
	# 	return self.__name + self.__address + str(self.__score) + self.__station + str(self.__distance)

	def getStation(self):
		return self.__station

	def getDistance(self):
		return self.__distance

	def getTags(self):
		return self.__tags

	def asdict(self):
		return {
			'name': self.getName(),
			'address': self.getAddress(),
			'score': self.getScore(),
			'station': self.getStation(),
			'distance': self.getDistance(),
			'tags': self.getTags()
		}

class Hotel(Facility):
	def __init__(self, name, address, score, star, distance):
		super(Hotel, self).__init__(self, name, address, score)
		self.__star = star
		self.__distance = distance

  #def __str__(self):
  #  return self.__name + self.__address + str(self.__score) + self.__star + str(self.__distance)

	def getStar(self):
		return self.__star

	def getDistance(self):
		return self.__distance

	def asdict(self):
		return {
			'name': self.__name,
	      		'address': self.__address,
	      		'score': self.__score,
	      		'star': self.__star,
	      		'distance': self.__distance
	    		}
		
