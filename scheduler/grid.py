import csv

class Decoder(object):
	"""This thing converts grids to other grids"""
	def __init__(self):
		print("decoder init")

	def makeHeader(self, grid):
		grid.write('type')
		i = 0
		time = 0
		dayList = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
		day = 0
		while i < 336:
			grid.write(",%s-%04d"%(dayList[day],time))
			if i % 2 == 0:
				time += 30
			else:
				time += 70
			if time == 2400:
				time = 0
				day += 1
			i+=1
		grid.write('\n')

	def getSurgeries(self, department, need):
		surgList = []
		# THIS SHOULD JUST BE DONE AT RUNTIME NOT IN A METHOD
		i = 0
		while i < need:
			# get a new surgery and add it to the list
			surgList.append('112')
			i+=1
		return surgList

	def parseBlock(self, blockGrid):
		dFile = 'departmentGrid.csv'
		# initialize the file
		dGrid = open(dFile, 'w+')
		self.makeHeader(dGrid)

		# get the information from the file object
		blockReader = csv.reader(blockGrid)


		blockReader.__next__()
		# populate the new file
		dList = []
		for row in blockReader:
			i = 0
			while i < len(row):
				if row[i] not in dList:
					dList.append(row[i])
				i+=2
		for d in dList:
			dGrid.write(d)
			dGrid.write(",0"*336)
			dGrid.write('\n')

		# now actually populate the file
		
		dGrid.close()
		return dFile

	def parseDepartment(self, departmentGrid):
		sFile = 'surgeryGrid.csv'
		# initialize the file
		sGrid = open(sFile, 'w+')
		self.makeHeader(sGrid)

		depMix = 'depCPT.csv'
		depCPT = open(depMix)

		# get the information from the file object
		reader = csv.reader(departmentGrid)
		# skip the header
		reader.__next__()

		# populate the new file
		sList = []
		for row in reader:
			# you have to make everything integer so we can get a sum to get list of surgeries
			depTimes = [row[0]]
			depTimes.extend([int(x) for x in row[1:]])

			sumSurgeries = sum(depTimes[1:])
			someSurgeries = self.getSurgeries(depTimes[0], sumSurgeries)

			# THIS ISNT RIGHT - NEED A ROW/COLUMN INCREMENTER METHOD


		return sFile


	def parseSurgery(self, surgeryGrid):
		tFile = 'trayGrid.csv'
		# initialize the file
		tGrid = open(tFile, 'w+')
		self.makeHeader(tGrid)

		# get the information from the file object
		reader = csv.reader(surgeryGrid)

		# populate the new file
		tList = []

		return tFile


if __name__ == '__main__':
	decoder = Decoder()
	blockGrid = open("block.csv")
	departmentFile = decoder.parseBlock(open('block.csv'))
	# surgeryFile = decoder.parseDepartment(open(departmentFile))
	# trayFile = decoder.parseSurgery(open(surgeryFile))






