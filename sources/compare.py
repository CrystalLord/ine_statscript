#
# Filename: compare.py
#
# Author: /u/CrystalLord
#
#
from csv_printer import CSVPrinter

DRY_RUN = False

def compare_main():
	try:	
		print("Compare 2 INE matrices")
		print("----------------------")
		pathA = "../ine_logs/"+str(input("Filename of previous month matrix> "))
		pathB = "../ine_logs/"+str(input("Filename of new month matrix> "))
		output = compare(pathA, pathB)
	except IOError:
		print("Invalid file path or access restricted. Closing script.")

def compare(pathA, pathB):
	'''
	TODO: Documentation
	'''
	fileA = open(pathA, "r")
	dataA = fileA.read()
	fileA.close()
	entriesA = dataA.split("\n")
	matrixA = [x.split(",") for x in entriesA]

	fileB = open(pathB, "r")
	dataB = fileB.read()
	fileB.close()
	entriesB = dataB.split("\n")
	matrixB = [x.split(",") for x in entriesB]

	printer = CSVPrinter()
	printer.set_timestamp(matrixA[0][0]+"/"+matrixB[0][0])
	printer.set_header(matrixA[1])

	resized_matrixA, resized_matrixB = resize_csv(matrixA[2:], matrixB[2:])

	for i in range(len(resized_matrixB)):
		printer.append_csv([
			resized_matrixB[i][0],
			resized_matrixB[i][1],
			-compare_values(resized_matrixA[i][2], resized_matrixB[i][2], "int"),
			compare_values(resized_matrixA[i][3], resized_matrixB[i][3], "int"),
			compare_values(resized_matrixA[i][4], resized_matrixB[i][4], "int"),
			health_compare(resized_matrixA[i][5], resized_matrixB[i][5]),
			round(compare_values(resized_matrixA[i][6], resized_matrixB[i][6], "float"), 3),
			round(compare_values(resized_matrixA[i][7], resized_matrixB[i][7], "float"), 3),
			])
	
	
	if not DRY_RUN:
		filename = "../ine_logs/"+matrixA[0][0]+"_"+matrixB[0][0]+"_comparison.csv"
		f = open(filename, "w")
		f.write(printer.output_csv())
		f.close()
		print("-------------------------")
		print("CSV printed to: "+filename)
		print("-------------------------")
	else:
		print("-------------------------")
		print("Dry run, no output printed")
		print("-------------------------")

def resize_csv(matrixA, matrixB):
	'''
	Returns 2 matrices that are both the same size, generated from matrixA and matrixB
		
		@param
		-matrixA: first matrix
		-matrixB: second matrix

		@return
		Returns 2 matrices that are the same length, but not necessarily the length
		of either A or B.
	'''
	
	resized_matrixA = matrixA[:]
	resized_matrixB = matrixB[:]

	i = 0
	while i < max(len(resized_matrixA), len(resized_matrixB)):
		if i >= len(resized_matrixB) and i < len(resized_matrixA):
			resized_matrixB.append([
				resized_matrixA[i][0], # Tab
				resized_matrixA[i][1], # Name
				"-", # Rank
				"-", # Subscribers
				"-", # Submission Count
				"-", # Health
				"-", # posts per subs
				"-", # % mods
				])
			continue
			i += 1
		if i >= len(resized_matrixA) and i < len(resized_matrixB):
			resized_matrixA.append([
				resized_matrixB[i][0], # Tab
				resized_matrixB[i][1], # Name
				"-", # Rank
				"-", # Subscribers
				"-", # Submission Count
				"-", # Health
				"-", # posts per subs
				"-", # % mods
				])
			continue
			i += 1
		
		# Check if they are the same subreddits
		try:
			if resized_matrixA[i][1] != resized_matrixB[i][1]:
				if len(resized_matrixB) > len(resized_matrixA):
					resized_matrixA.insert(i,[
						resized_matrixB[i][0], # Tab
						resized_matrixB[i][1], # Name
						"-", # Rank
						"-", # Subscribers
						"-", # Submission Count
						"-", # Health
						"-", # posts per subs
						"-", # % mods
						])
				else:
					resized_matrixB.insert(i,[
						resized_matrixA[i][0], # Tab
						resized_matrixA[i][1], # Name
						"-", # Rank
						"-", # Subscribers
						"-", # Submission Count
						"-", # Health
						"-", # posts per subs
						"-", # % mods
						])
		except IndexError:
			resized_matrixA = resized_matrixA[:-1]
			resized_matrixB = resized_matrixB[:-1]
			break
		# Increment
		i += 1
	return resized_matrixA, resized_matrixB

def compare_values(valueA, valueB, value_type):
	'''
	Provides a difference comparison that still works for a variety of values.
		
		@param
		-valueA: Starting value
		-valueB: Ending value
		-value_type: A string that describes the type of data. Can be int or float

		@return
		Returns the difference of the 2 values.
	'''
	if valueA == "-" or valueA == "FORBIDDEN" or valueA == "NOT FOUND":
		valueA = 0
	if valueB == "-" or valueB == "FORBIDDEN" or valueB == "NOT FOUND":
		valueB = 0

	if value_type == "int":
		return int(valueB)-int(valueA)
	elif value_type == "float":
		return float(float(valueB)-float(valueA))

def health_compare(healthA, healthB):
	if healthA == "healthy" and healthB == "unhealthy":
		return "h -> u"
	elif healthA == "unhealthy" and healthB == "healthy":
		return "u -> h"
	elif healthA == "critical" and healthB == "unhealthy":
		return "c -> u"
	elif healthA == "healthy" and healthB == "critical":
		return "h -> c"
	elif healthA == "critical" and healthB == "healthy":
		return "c -> h"
	elif healthA == "unhealthy" and healthB == "critical":
		return "u -> c"
	else:
		return "-"

# Main Trick
if __name__ == "__main__":
	compare_main()
