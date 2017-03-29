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
		print("DATABASE RESET!\n")

	def getTraysForCart(self, orcc):
		query = 'select (Tray_id) from trays where (ORCC) like %d' % orcc
		print(query)
		resList = self.execute(query)
		for res in resList:
			print(res)


	def uploadInstruments(self, filename):
		# tray name, inst name, inst id, qty
		orders = []
		with open(filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			next(reader) # skip headers
			for row in reader:
				insert = 'INSERT INTO instruments VALUES({}, "{}", {}, "{}")'.format(row[3], row[2], row[4], row[0])
				# print(insert)
				orders.append(insert)

		self.execute(orders)
		print("Instruments uploaded")

	def uploadTrays(self, filename):
		# trayID, trayName, orcc, tray quantity
		# assume we are receiving a csv of those four things for now - not parse yet
		orders = []
		with open(filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			next(reader) # skip headers
			for row in reader:
				insert = 'INSERT INTO trays VALUES ({}, "{}", {}, {})'.format(row[3], row[2].replace("'", '"'), row[0], row[4])
				print(insert)
				orders.append(insert)

		self.execute(orders)
		print("Trays uploaded")

	def uploadProcedures(self, filename):
		# CPT, name, orcc
		orders = []
		with open(filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			next(reader) # skip headers
			for row in reader:
				insert = 'INSERT INTO procedures VALUES ({}, "{}", {})'.format(row[0], row[2], row[5])
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
					resList.append(cursor.execute(cmd))
		return resList

if __name__ == '__main__':
	demon = SQLDemon('root', '')

	# demon.resetDB()
	# instData = "/Users/ewbrower/Documents/SeniorDesign/data/pick_tick_translation.csv"
	# demon.uploadInstruments(instData)
	# caseData = "/Users/ewbrower/Documents/SeniorDesign/data/cases.csv"
	# demon.uploadProcedures(caseData)
	# trayData = "/Users/ewbrower/Documents/SeniorDesign/data/trays.csv"
	# demon.uploadTrays(trayData)

	demon.getTraysForCart(26665)










