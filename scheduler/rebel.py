import csv
import datetime
import random
import pymysql

class Thinker(object):
	"""This thing thinks really hard about an easy problem"""

	def __init__(self):
		self.connection = pymysql.connect(host='',
                            user='root',
                            password='',
                            db='va_inventory',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor,
                            autocommit=True)

	def getDepartmentDict(self, filename):
		reader = csv.reader(open(filename))
		headers = ['M', 'T', 'W', 'R', 'F']
		reader.__next__()

		# this dictionary describes how many surgeries per department per room per day
		departDayRooms = {}
		for day in headers:
			departDayRooms[day] = []
		for row in reader:
			i = 0
			while i < 5:
				day = headers[i]
				department = row[i*2]
				count = row[i*2 + 1]
				timeList = self.getDepartmentTimes(int(count), day)
				departDayRooms[day].append((department, timeList))
				i+=1
		return departDayRooms

	def getDepartmentTimes(self, count, day):
		i = 0

		time = datetime.datetime(1,1,1,8)
		delta = datetime.timedelta(minutes=30)

		depTimes = []
		rate = round(16/count) # this is how many 30 minute increments until next (until end of day)
		# print("count " + str(count) + " -> time of surgery " + str(rate/2) + " hours")
		j = 0
		while i < count:
			fTime = str(day + "-%02d"%time.hour + "%02d"%time.minute)
			depTimes.append(fTime)
			time+=delta*rate
			i+=1
		# print(depTimes)
		return depTimes

	def getSurgeryDict(self, depDict):
		timeDict = {}
		surgeryDayRooms = depDict
		for day in surgeryDayRooms.keys():
			for department in surgeryDayRooms[day]:
				i = 0
				while i < len(department[1]):
					surgery = self.getRandomSurgery(department[0])
					time = department[1][i]
					department[1][i] = (surgery, time)
					if time not in timeDict.keys():
						timeDict[time] = [surgery]
					else:
						timeDict[time].append(surgery)
					i+=1
				# print(department)
		# print(surgeryDayRooms)
		return timeDict

	def getRandomSurgery(self, department):
		# print('getting random %s surgery'%department)
		# HAD TO ADD IN ORAL MANUALLY -- MUST FIX
		depReader = csv.reader(open('depCPT.csv'))
		rn = random.random()
		for row in depReader:
			if row[0] == department and float(row[4]) > rn:
				return row[1]

	def createGrid(self, times, filename):
		# initialize the file
		dGrid = open(filename, 'w+')
		headers = self.makeHeader(dGrid)

		# get all surgeries performed in a week
		allSurgeries = []
		for key in times.keys():
			for item in times[key]:
				if item not in allSurgeries:
					allSurgeries.append(item)

		# need a special method to get all trays with no repeats
		allTrays = self.getTrays(allSurgeries)
		for tray in allTrays:
			dGrid.write(tray)
			for i, tSlice in enumerate(headers[1:]):
				dGrid.write(',0')
			dGrid.write('\n')


	def getTrays(self, surgeries):
		tList = []
		with self.connection.cursor() as cursor:
			for surgery in surgeries:
				query = "SELECT t.Tray_id from procedures p INNER JOIN trays t on t.orcc = p.orcc WHERE p.CPT = %s" % surgery
				# print(query)
				cursor.execute(query)
				if cursor.rowcount != 0:
					output = cursor.fetchall()
					# print(output)
					for tray in output:
						if tray['Tray_id'] not in tList:
							tList.append(str(tray['Tray_id']))
		return tList

	def makeHeader(self, grid):
		grid.write('type')
		i = 0
		time = 0
		dayList = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
		day = 0
		slices = ['type']
		while i < 336:
			timeSlice = "%s-%04d"%(dayList[day],time)
			slices.append(timeSlice)
			grid.write(',' + timeSlice)
			if i % 2 == 0:
				time += 30
			else:
				time += 70
			if time == 2400:
				time = 0
				day += 1
			i+=1
		grid.write('\n')
		return slices


if __name__ == '__main__':
	thinker = Thinker()
	depDict = thinker.getDepartmentDict('block.csv')
	timeDict = thinker.getSurgeryDict(depDict)
	# print(timeDict)
	thinker.createGrid(timeDict, 'grid.csv')












