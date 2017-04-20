import csv
import datetime as dt
import random
import pymysql
import operator

connection = pymysql.connect(host='',
                        user='root',
                        password='',
                        db='va_inventory',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor,
                        autocommit=True)
cursor = connection.cursor()

procedos = []
missing = []

def getKeys():
	i = 0
	time = 0
	dayList = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
	day = 0
	slices = []
	while i < 336:
		timeSlice = "%s-%04d"%(dayList[day],time)
		slices.append(timeSlice)
		if i % 2 == 0:
			time += 30
		else:
			time += 70
		if time == 2400:
			time = 0
			day += 1
		i+=1
	return slices

def addSurgery(start, end, department, count, day):
	i = 0

	time = dt.datetime(1,1,1,8)
	hours = dt.timedelta(hours = 8)
	delta = 30

	# calculation for surgery length
	length = hours/count - dt.timedelta(minutes = (hours/count).seconds/60 % delta)
	# print(str(count) + " " + str(length))

	while i < count:
		# start time = time
		sTime = str(day + "-%02d"%time.hour + "%02d"%time.minute)

		# end time = time + length of surgery
		time+=length
		eTime = str(day + "-%02d"%time.hour + "%02d"%time.minute)
		# print(sTime + " -> " + eTime)

		surgery = getRandomSurgery(department)

		if sTime in start.keys():
			start[sTime].append((department, surgery))
		else:
			start[sTime] = [(department, surgery)]

		if eTime in end.keys():
			end[eTime].append((department, surgery))
		else:
			end[eTime] = [(department, surgery)]
		i+=1

def getRandomSurgery(department):
	# print('getting random %s surgery'%department)
	# HAD TO ADD IN ORAL MANUALLY -- MUST FIX
	depReader = csv.reader(open('data/depCPT.csv'))
	rn = random.random()
	for row in depReader:
		if row[0] == department and float(row[4]) > rn:
			if row[1] not in procedos:
				procedos.append(row[1])
			return row[1]

def generateSurgeryDictionary(blockFile):
	# potentialKeys = getKeys()
	# print(potentialKeys)
	reader = csv.reader(open(blockFile))
	reader.__next__()

	days = ['M', 'T', 'W', 'R', 'F']

	start = {}
	end = {}

	for row in reader:
		i = 0
		while i < 5:
			day = days[i]
			department = row[i*2]
			count = row[i*2 + 1]
			addSurgery(start, end, department, int(count), day)
			i+=1

	surgeryDayRooms = {'start':start, 'end':end}
	return surgeryDayRooms

def getInitialRow():
	return [0]*336

def getTimes():
	dayList = ['M', 'T', 'W', 'R', 'F', 'S', 'U']

	times = []
	i = 0
	time = 0
	day = 0
	while i < 336:
		timeSlice = "%s-%04d"%(dayList[day],time)
		times.append(timeSlice)
		if i % 2 == 0:
			time += 30
		else:
			time += 70
		if time == 2400:
			time = 0
			day += 1
		i+=1
	return times

def generateTrayDictionary(surgeryDict):
	startTrays = convertSurgeryTimes(surgeryDict, 'start')
	endTrays = convertSurgeryTimes(surgeryDict, 'end')
	trays = startTrays
	trays.update(endTrays)
	return trays

def convertSurgeryTimes(sDict, key):
	trays = {}
	times = getKeys()

	for timeSlice in sDict[key].keys():
		tIndex = times.index(timeSlice)
		surgeries = sDict[key][timeSlice]
		for depSurgeTup in surgeries:
			surgery = depSurgeTup[1]
			surgTrays = getTrayCounts(surgery)
			if surgTrays:
				for tray in surgTrays.keys():
					trayName = str(tray) + '-' + key
					if trayName not in trays.keys():
						trays[trayName] = getInitialRow()
					trays[trayName][tIndex] += surgTrays[tray]
	return trays

def getTrayCounts(surgery):
	query = "SELECT t.Tray_id, t.T_QTY from procedures p INNER JOIN trays t on t.orcc = p.orcc WHERE p.CPT = %s" % surgery
	cursor.execute(query)
	if cursor.rowcount != 0:
		output = cursor.fetchall()
		tDict = {}
		for tray in output:
			tDict[tray['Tray_id']] = tray['T_QTY']
		return tDict
	else:
		# this means the surgery has no trays
		if surgery not in missing:
			missing.append(surgery)
	return {}

def makeGrid(trays, filename):
	grid = open(filename, 'w+')
	allTrays = getBothTrays()
	starts = allTrays['start']
	ends = allTrays['end']

	# this sorts them by the TRAY ID from smallest to largest
	starts.sort(key = lambda x: x.split('-')[0])
	ends.sort(key = lambda x: x.split('-')[0])
	for tray in starts:
		if tray not in trays.keys():
			initRow = getInitialRow()
			for x in initRow:
				grid.write(str(x) + ',')
		else:
			for x in trays[tray]:
				grid.write(str(x) + ',')
	grid.write('\n')
	for tray in ends:
		if tray not in trays.keys():
			initRow = getInitialRow()
			for x in initRow:
				grid.write(str(x) + ',')
		else:
			for x in trays[tray]:
				grid.write(str(x) + ',')
	grid.close()

def makeNice(trays, filename):
	grid = open(filename, 'w+')
	grid.write('type')
	i = 0
	time = 0
	dayList = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
	day = 0
	while i < 336:
		timeSlice = "%s-%04d"%(dayList[day],time)
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
	allTrays = getBothTrays()
	starts = allTrays['start']
	ends = allTrays['end']

	# this sorts them by the TRAY ID from smallest to largest
	starts.sort(key = lambda x: x.split('-')[0])
	ends.sort(key = lambda x: x.split('-')[0])
	for tray in starts:
		grid.write(tray + ',')
		if tray not in trays.keys():
			initRow = getInitialRow()
			for x in initRow:
				grid.write(str(x) + ',')
		else:
			for x in trays[tray]:
				grid.write(str(x) + ',')
		grid.write('\n')
	for tray in ends:
		grid.write(tray + ',')
		if tray not in trays.keys():
			initRow = getInitialRow()
			for x in initRow:
				grid.write(str(x) + ',')
		else:
			for x in trays[tray]:
				grid.write(str(x) + ',')
		grid.write('\n')
	grid.close()

def getAllTrays():
	query = "SELECT DISTINCT Tray_id from trays"
	cursor.execute(query)
	allTrays = []
	for t in cursor.fetchall():
		allTrays.append(str(t['Tray_id']) + '-start')
		allTrays.append(str(t['Tray_id']) + '-end')
	return allTrays

def getBothTrays():
	query = "SELECT DISTINCT Tray_id from trays"
	cursor.execute(query)
	starts = []
	ends = []
	for t in cursor.fetchall():
		starts.append(str(t['Tray_id']) + '-start')
		ends.append(str(t['Tray_id']) + '-end')
	return {'start': starts, 'end': ends}

def getSample(filename):
	sDict = generateSurgeryDictionary(filename)
	tDict = generateTrayDictionary(sDict)
	makeNice(tDict, 'schedules/sample.csv')

if __name__ == '__main__':
	# before doing any of this, you have to create the database
	# use the scripe.py script

	blockedSchedule = 'data/block.csv'

	# make an example schedule that is human readable
	getSample(blockedSchedule)

	# make any 'number' of schedules that will be read into the IP
	number = 10
	i = 0
	while i < number:
		print("creating file " + str(i))
		sDict = generateSurgeryDictionary(blockedSchedule)
		tDict = generateTrayDictionary(sDict)
		makeGrid(tDict, 'schedules/sortedTraySchedule%02d.csv'%i)
		i+=1






