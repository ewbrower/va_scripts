import csv
import pymysql

class SQLDemon(object):
	"""something that uploads to the database neatly"""
	def __init__(self, user, word):
		super(SQLDemon, self).__init__()
		self.connection = pymysql.connect(host='',
                            user=user,
                            password=word,
                            db='va_inventory',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor,
                            autocommit=True)

	def resetDB(self):
		with open("reset.sql", 'r') as reset:
			sql = reset.read()
			commands = sql.split(';')
			# commands = [str(c.strip()) + ";" for c in commands]
		self.execute(commands[:-1]) # the last one is a blank command
		print("DATABASE RESET!")

	def getTraysForCart(self, orcc):
		query = 'select (Tray_id) from trays where (ORCC) like %d' % orcc
		print(query)
		resList = self.execute(query)
		for res in resList:
			print(res)


	def uploadInstruments(self, filename):
		# tray name, inst name, inst id, qty
		orders = []
		with open(filename, 'r', encoding='ISO-8859-1') as csvfile:
			reader = csv.reader(csvfile)
			next(reader) # skip headers
			for row in reader:
				if not row[0]:
					pass
				else:
					insert = 'INSERT INTO instruments VALUES("{}", "{}", {}, "{}")'.format(row[3], row[2], row[4], row[0])
					orders.append(insert)

		self.execute(orders)
		print("Instruments uploaded")

	def uploadTrays(self, filename):
		# trayID, trayName, orcc, tray quantity
		# assume we are receiving a csv of those four things for now - not parse yet
		orders = []
		with open(filename, 'r', encoding='ISO-8859-1') as csvfile:
			reader = csv.reader(csvfile)
			next(reader) # skip headers
			for row in reader:
				insert = 'INSERT INTO trays VALUES ({}, "{}", {}, {})'.format(row[3], row[2].replace("'", '"'), row[0], row[4])
				# print(insert)
				orders.append(insert)

		self.execute(orders)
		print("Trays uploaded")

	def uploadProcedures(self, filename):
		# CPT, name, orcc
		orders = []
		with open(filename, 'r', encoding='ISO-8859-1') as csvfile:
			reader = csv.reader(csvfile)
			next(reader) # skip headers
			for row in reader:
				# print(row)
				insert = 'INSERT INTO procedures VALUES ({}, "{}", {})'.format(row[1], row[2], row[4])
				# print(insert)
				orders.append(insert)

		self.execute(orders)
		print("Procedures uploaded")

	def execute(self, commands):
		resList = []
		with self.connection.cursor() as cursor:
			if isinstance(commands, str):
				resList.append(cursor.execute(commands))
			else:
				for cmd in commands:
					try:
						resList.append(cursor.execute(cmd))
					except (pymysql.err.IntegrityError):
						# print('skipped duplicate entry\n' + cmd + '\n')
						pass
					finally:
						print(cmd)
		return resList

if __name__ == '__main__':
	demon = SQLDemon('root', '')

	demon.resetDB()
	instData = "data/instruments.csv"
	demon.uploadInstruments(instData)

	caseData = "data/FullSurgery.csv"
	demon.uploadProcedures(caseData)

	trayData = "data/trays.csv"
	demon.uploadTrays(trayData)











