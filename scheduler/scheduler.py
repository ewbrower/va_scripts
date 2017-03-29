import csv

departments = ["ORTHO", "OPTHAMOLOGY", "CARDIAC", "GYN", "PODIATRY", "ENT", "GU", "VASC", 
	"ORTH_HAND", "GEN", "NEURO", "PLASTIC", "THORACIC"]

class Day(object):
	"""This represents the surgeries and surgery times of a particular day"""
	def __init__(self, departs, coverage):
		print("new day")
		print(departs)

	def getName(self):
		return "Monday"
		

class BlockSchedule(object):
	"""This represents the data that comprises a block schedule of one week"""

	def __init__(self, filename):
		print("File selected: " + str(filename))
		datafile = open(filename)

		self.coverage = 8 # need to find
		self.days = []
		self.createDays(datafile)
		# print(self.coverage)

	def createDays(self, datafile):
		reader = csv.reader(datafile)
		index = 0
		tempDays = []
		row = reader.__next__()
		while index < len(row):
			tempDays.append({"name": row[index], "surgeries": []})
			index+=2
		print(tempDays)
		for row in reader:
			index = 0
			day = 0
			while index < len(row):
				tempDays[day]["surgeries"].append((row[index],row[index+1]))
				day+=1
				index+=2
		print(tempDays[0])
		for day in tempDays:
			self.days.append(Day(day, 8))

if __name__ == '__main__':
	block = BlockSchedule("block.csv")









