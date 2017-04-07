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

# list of the surgeries that don't have trays
missing = []
procedos = []

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
	depReader = csv.reader(open('/Users/ewbrower/git/va_scripts/data/depCPT.csv'))
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
	# print(surgeryDict)
	# print(getTimes())
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
		# print(timeSlice)
		surgeries = sDict[key][timeSlice]
		# print(str(timeSlice) + " " + str(surgeries))
		for depSurgeTup in surgeries:
			surgery = depSurgeTup[1]
			surgTrays = getTrayCounts(surgery)
			if surgTrays:
				# print(surgTrays)
				for tray in surgTrays.keys():
					# print(tray)
					trayName = str(tray) + '-' + key
					if trayName not in trays.keys():
						trays[trayName] = getInitialRow()
					trays[trayName][tIndex] += surgTrays[tray]
			# else:
			# 	print(depSurgeTup)
	return trays

def getTrayCounts(surgery):
	query = "SELECT t.Tray_id, t.T_QTY from procedures p INNER JOIN trays t on t.orcc = p.orcc WHERE p.CPT = %s" % surgery
	# print(query)
	cursor.execute(query)
	# print(cursor.fetchall)
	if cursor.rowcount != 0:
		output = cursor.fetchall()
		# print(output)
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
	# grid.write('type')
	# i = 0
	# time = 0
	# dayList = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
	# day = 0
	# while i < 336:
	# 	timeSlice = "%s-%04d"%(dayList[day],time)
	# 	grid.write(',' + timeSlice)
	# 	if i % 2 == 0:
	# 		time += 30
	# 	else:
	# 		time += 70
	# 	if time == 2400:
	# 		time = 0
	# 		day += 1
	# 	i+=1
	# grid.write('\n')
	allTrays = getBothTrays()
	starts = allTrays['start']
	ends = allTrays['end']
	# print(allTrays)
	# print(trays.keys())
	# this sorts them by the TRAY ID from smallest to largest
	starts.sort(key = lambda x: x.split('-')[0])
	ends.sort(key = lambda x: x.split('-')[0])
	# print(trays)
	for tray in starts:
		# print(tray)
		# grid.write(tray + ',')
		if tray not in trays.keys():
			# print(tray)
			initRow = getInitialRow()
			for x in initRow:
				grid.write(str(x) + ',')
		else:
			for x in trays[tray]:
				grid.write(str(x) + ',')
	grid.write('\n')
	for tray in ends:
		# grid.write(tray + ',')
		if tray not in trays.keys():
			# print(tray)
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
	# print(allTrays)
	# print(trays.keys())
	# this sorts them by the TRAY ID from smallest to largest
	starts.sort(key = lambda x: x.split('-')[0])
	ends.sort(key = lambda x: x.split('-')[0])
	# print(trays)
	for tray in starts:
		# print(tray)
		grid.write(tray + ',')
		if tray not in trays.keys():
			# print(tray)
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
			# print(tray)
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
	sDict = generateSurgeryDictionary('block.csv')
	tDict = generateTrayDictionary(sDict)
	makeNice(tDict, filename)

if __name__ == '__main__':
	# print(tDict)
	i = 0
	getSample('samples/sample.csv')
	while i < 100:
		print("creating file " + str(i))
		sDict = generateSurgeryDictionary('block.csv')
		tDict = generateTrayDictionary(sDict)
		makeGrid(tDict, 'traySchedules/sortedTraySchedule%02d.csv'%i)
		i+=1

	for miss in sorted(missing):
		print(miss)
	# print(sorted(procedos))






