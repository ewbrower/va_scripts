import pymysql

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


if __name__ == '__main__':
	# orccList = [26123,26615,27447,27880,28290,28810,31287,31536,35301,39402,44160,46999,47562,49505,49505,49650,52356,52601,52632,58555,64721,69703]
	# surg = getSurgeries(orccList)
	# print(getCourtsInfo())
	print(getProcedures())
