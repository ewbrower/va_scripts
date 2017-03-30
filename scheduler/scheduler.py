import csv

departments = ["ORTHO", "OPTHAMOLOGY", "CARDIAC", "GYN", "PODIATRY", "ENT", "GU", "VASC", 
	"ORTH_HAND", "GEN", "NEURO", "PLASTIC", "THORACIC"]

class Day(object):
	"""This represents the surgeries and surgery times of a particular day"""
	def __init__(self, dayDict, coverage):
		# print("new day")
		# print(dayDict)
		self.name = dayDict["name"]
		{"surgery": "ORTH", "start": 800, "end": 1200}
		self.schedule = self.generateSchedule(dayDict["surgeries"], coverage)

	def getName(self):
		return self.name

	def getTrayPerSurgery(self, cpt):
		return "SELECT (t.Tray_id, t.tray, t.T_QTY) from procedures p INNER JOIN trays t on t.orcc = p.orcc WHERE p.CPT = %s" % cpt

	def generateSchedule(self, departCounts, coverage):
		hoursInDay = 8
		print(departCounts)
		for departmentCount in departCounts:
			surgRate = round(hoursInDay / int(departmentCount[1]) * 2) / 2
			print(str(departmentCount[0]) + " " + str(departmentCount[1]) + " -> " + str(surgRate))
			print(str(surgRate % 8))

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
		# print(tempDays)
		for row in reader:
			index = 0
			day = 0
			while index < len(row):
				tempDays[day]["surgeries"].append((row[index],row[index+1]))
				day+=1
				index+=2
		# print(tempDays[0])
		for day in tempDays:
			self.days.append(Day(day, 8))

	def getDays(self):
		return self.days

class Decoder(object):
	"""This object transforms departments into specific surgeries"""
	def __init__(self, blockSchedule):
		self.blockSchedule = blockSchedule
		
	def getTrayDemand(self):
		""" per block schedule, return the tray names, quantities, and times needed """
		return "trays"

if __name__ == '__main__':
	block = BlockSchedule("block.csv")
	for day in block.getDays():
		print(day.getName())
	decoder = Decoder(block)
	# print(decoder.getTrayDemand())










