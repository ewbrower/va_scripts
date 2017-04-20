import pymysql
from itertools import chain, combinations

connection = pymysql.connect(host='',
                        user='root',
                        password='',
                        db='va_inventory',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor,
                        autocommit=True)
cursor = connection.cursor()

def getSurgeries(orccList):
	# query = 'SELECT * FROM trays'
	for interest in orccList:
		query = 'SELECT name, ORCC FROM procedures WHERE CPT = %s' % interest
		print(query)
		cursor.execute(query)
		print(cursor.fetchall())
	return orccList

def getCourtsInfo():
	# most used trays based on surgery data
	return 'here you go Court'

def getProcedures():
	query = 'select CPT from procedures'
	cursor.execute(query)
	proc = []
	for item in cursor.fetchall():
		proc.append(item['CPT'])
	return sorted(proc)

def getTrayNames():
	query = 'select distinct Tray_id, tray from trays'
	cursor.execute(query)
	listed = []
	for tray in cursor.fetchall():
		# print(tray['tray'])
		listed.append((tray['Tray_id'], tray['tray']))
	# print(listed)
	listed.sort(key = lambda t: t[0])
	with open('trayDictionary.csv', 'w+') as trandel:
		for tup in listed:
			print(tup)
			trandel.write(str(tup[0]) + ',' + tup[1] + '\n')

def get2TrayOverlap(tup):
	query = 'select t1.ORCC from trays t1, trays t2 where t1.ORCC = t2.ORCC and t1.Tray_id = %d and t2.Tray_id = %d' %(tup[0], tup[1])
	print(query)
	cursor.execute(query)
	return cursor.fetchall()


def getOverlap(interest):
	xs = list(interest)
	combi = list(chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1)))

	for item in combi:
		if len(item) == 2:
			# print(item)
			res = get2TrayOverlap(item)
			for thing in res:
				print(thing)
		elif len(item) == 3:
			pass

if __name__ == '__main__':
	# surg = getSurgeries(orccList)
	# print(getCourtsInfo())
	# print(getProcedures())
	# getTrayNames()
	major = 26947
	minor = 27967
	plastic = 26011
	trayInterest = [major, minor, plastic]
	getOverlap(trayInterest)










