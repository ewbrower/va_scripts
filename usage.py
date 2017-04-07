import csv

def getDemand(blockFile, depCPT, trayFile):
	# print('demand')
	depDemand, depPercent = getDepartmentDemand(blockFile)
	print(depPercent)
	# tReader = csv.reader(open(trayFile))
	surgLikely = getSurgeryPercent(depCPT, depPercent)
	# print(surgLikely)
	# print(sum(surgLikely.values()))
	for key in surgLikely.keys():
		print(key + ", " + str(surgLikely[key]))

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
	print(reader.__next__())
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

if __name__ == '__main__':
	getDemand('scheduler/block.csv','data/depCPT.csv','data/TRAYS.csv')













