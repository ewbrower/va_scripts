import csv
import datetime as dt
import random
import pymysql

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
	depReader = csv.reader(open('depCPT.csv'))
	rn = random.random()
	for row in depReader:
		if row[0] == department and float(row[4]) > rn:
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
	return ['0']*336

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
	trays = {}
	convertSurgeryTimes(surgeryDict, 'start', trays)
	convertSurgeryTimes(surgeryDict, 'end', trays)
	# print(trays)

def convertSurgeryTimes(sDict, key, trays):
	connection = pymysql.connect(host='',
                            user='root',
                            password='',
                            db='va_inventory',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor,
                            autocommit=True)
	cursor = connection.cursor()
	for timeSlice in sDict[key].keys():
		surgeries = sDict[key][timeSlice]
		for sTuple in surgeries:
			orcc = sTuple[1]
			# print(timeSlice + "->" + orcc)
			needed = getTrayCounts(cursor, orcc)
			if not needed:
				# print("No trays for ORCC %s"% orcc)
				pass
			else:
				print(timeSlice + " -> " + str(needed))
		# trays[timeSlice] = 0

def getTrayCounts(cursor, surgery):
	query = "SELECT t.Tray_id, t.T_QTY from procedures p INNER JOIN trays t on t.orcc = p.orcc WHERE p.CPT = %s" % surgery
	# print(query)
	cursor.execute(query)
	if cursor.rowcount != 0:
		output = cursor.fetchall()
		# print(output)
		tDict = {}
		for tray in output:
			tDict[tray['Tray_id']] = tray['T_QTY']
		return tDict
	return []

if __name__ == '__main__':
	sDict = generateSurgeryDictionary('block.csv')
	tDict = generateTrayDictionary(sDict)












