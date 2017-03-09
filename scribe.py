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
                            cursorclass=pymysql.cursors.DictCursor)

	def uploadInstruments(self, filename):
		cursor = self.connection.cursor()
		# print(cursor.database)
		orders = []
		with open(filename, 'r') as csvfile:
			reader = csv.reader(csvfile)
			next(reader)
			for row in reader:
				insert = 'INSERT INTO instruments VALUES({}, "{}", {})'.format(row[0], row[1], row[2])
				print(insert)
				orders.append(insert)
		with self.connection.cursor() as cursor:
			for order in orders:
				res = cursor.execute(order)
				print(res)


if __name__ == '__main__':
	demon = SQLDemon('root', '')
	demon.uploadInstruments("sampleInstruments.csv")