#
# Filename: csv_printer.py
#
# Author: /u/CrystalLord
#
#

class CSVPrinter:
	def __init__(self):
		'''
		initialisation of the csv printer
		'''
		self.text = ""
		self.csv = '"Tab","Subreddit","Subscribers","Number of Posts","Health","Posts/subs"\n'

	def p(self, text):
		'''
		Kind of like print(), but also writes to the text buffer
			
			@param
			-text: text buffer
		'''
		self.text += text+'\n'
		print(text)
	
	def append_text(self, text):
		'''
		Append some text to the text buffer
		'''
		self.text += text+'\n'

	def append_csv(self, l):
		'''
		Append a csv line to the csv buffer
			
			@param
			-l: list of things to append in a csv like
			fashion
		'''
		# Iterate for each part of l
		for index in range(len(l)):
			# Make sure not to add a comma before the first element
			if index != 0:
				self.csv += ','
			
			# Check if a integer or float
			if isinstance(l[index], int) or isinstance(l[index], float):
				self.csv += str(l[index])
			else:
				# Surround with quotes if not either
				self.csv += '"'+str(l[index])+'"'

		# Add a newline after each entry
		self.csv += "\n"

	def output_text(self):
		return self.text
	
	def output_csv(self):
		return self.csv
