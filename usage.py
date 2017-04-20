import csv
import pymysql

connection = pymysql.connect(host='',
                        user='root',
                        password='',
                        db='va_inventory',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor,
                        autocommit=True)
cursor = connection.cursor()

def getDemand(blockFile, depCPT, trayFile):
	# print('demand')
	depDemand, depPercent = getDepartmentDemand(blockFile)
	# print(depPercent)
	# tReader = csv.reader(open(trayFile))
	surgLikely = getSurgeryPercent(depCPT, depPercent)
	print(surgLikely)
	print(sum(surgLikely.values()))
	# print(sum(surgLikely.values()))
	# for key in surgLikely.keys():
	# 	print(key + ", " + str(surgLikely[key]))
	trayLikely = getTrayPercent(surgLikely)
	trayList = []
	for key in trayLikely.keys():
		trayList.append((key, trayLikely[key]))
	trayList.sort(key = lambda x: x[1])
	# for item in trayList:
	# 	print(str(item[0]) + ', ' + str(item[1]))

def getDepartmentDemand(blockFile):
	reader = csv.reader(open(blockFile))
	reader.__next__()
	depDemand = {}
	for row in reader:
		i = 0
		while i < len(row):
			if row[i] not in depDemand:
				depDemand[row[i]] = int(row[i+1])
			else:
				depDemand[row[i]] += int(row[i+1])
			i+=2
	depPercent = {}
	weeklySurgeries = sum(depDemand.values())
	for key in depDemand.keys():
		depPercent[key] = depDemand[key] / weeklySurgeries
	return depDemand, depPercent

def getSurgeryPercent(depCPT, depPercent):
	reader = csv.reader(open(depCPT, encoding='ISO-8859-1'))
	reader.__next__()
	surgeries = {}
	priors =[1.0]
	index = 1

	for row in reader:
		dep = row[0]
		cpt = row[1]

		depLikely = float(depPercent[dep])
		surgLikely = float(row[5]) * depLikely

		if cpt in surgeries.keys():
			surgeries[cpt] += surgLikely
		else:
			surgeries[cpt] = surgLikely
	return surgeries

def getTrayPercent(surgLikely):
	trayPerc = {}
	for surg in surgLikely.keys():
		trays = getTrays(surg)
		# print(str(surg) + ' -> ' + str(trays))
		for tray in trays:
			if tray not in trayPerc:
				trayPerc[tray] = surgLikely[surg]
			else:
				trayPerc[tray] += surgLikely[surg]
	# print(trayPerc)
	return trayPerc

def getTrays(surgery):
	query = "SELECT t.Tray_id, t.T_QTY from procedures p INNER JOIN trays t on t.orcc = p.orcc WHERE p.CPT = %s" % surgery
	# print(query)
	cursor.execute(query)
	# print(cursor.fetchall)
	if cursor.rowcount != 0:
		output = cursor.fetchall()
		# print(output)
		tDict = []
		for tray in output:
			tDict.append(tray['Tray_id'])
		return tDict
	return []

if __name__ == '__main__':
	getDemand('scheduler/block.csv','data/depCPT.csv','data/TRAYS.csv')













