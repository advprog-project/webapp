class Facility:
	def __init__(self, name, address, score):
		Facility.name = name 
		Facility.address = address
		Facility.score = score

class Restaurant(Facility):
	def __init__(self, name, address, score, tags, station, distance):
		Facility.__init__(self, name, address, score)
		self.tags = tags
		self.station = station
		self.distance = distance
	def __str__(self):
		return self.name + self.address + str(self.score) + self.station + str(self.distance)
	def getTags(self):
		for tag in self.tags:
			print(tag, " ", end="")
				
class Hotel(Facility):
	def __init__(self, name, address, score, star):
		Facility.__init__(self, name, address, score)
		self.star = star


# polymorphism for r&h
def sort:


""" exception
	readfile 
	thread: read two files in two threads"""
def readFile():
	try:
		lines = open("restaurant.csv")
		lines.readline()
		restaurants = []
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
				#print(restaurant)
				#restaurant.getTags()
				#print("")
				restaurants.append(restaurant)
	except IOError:
		print("Error: restaurant.csv does not exist or it can't be opened.")
	lines.close()	

#preprocess and search of the input
def search(input, object):
	
	
"""
#main part below
if name == '__main__':
	restaurant = Restaurant
