#
# Filename: network_health_bot.py
#
# Authors:
# -/u/CVance1
# -/u/CrystalLord
# -/u/m1dn1ght5un
#
#


import time
import praw
import sys

class Printer:
	def __init__(self):
		self.text = ""
		self.csv = '"Tab","Subreddit","Subscribers","Number of Posts","Health"\n'

	def p(self, text):
		self.text += text+'\n'
		print(text)
	
	def append_text(self, text):
		self.text += text+'\n'

	def append_csv(self, tab, subreddit, subscribers, health, num_of_posts):
		self.csv += '"'+tab+'","'+subreddit+'",'+str(subscribers)+','+str(num_of_posts)+',"'+health+'"\n'

	def output_csv(self):
		return self.text
	
	def output_csv(self):
		return self.csv

class HealthThreshold:
	def __init__(self, unhealthy=15, critical=5):
		self.unhealthy = unhealthy
		self.critical = critical
	
	def __repr__(self):
		'''
		Representation method
			
			@return
			Returns a representation in the form HealthThreshold(unhealthy,critical)
		'''
		s = "HealthThreshold("+str(self.unhealthy_post_count)+","+str(self.critical_post_count)+")"
		return s
	
	def rate_health(self, value):
		if value > self.unhealthy:
			return "healthy"
		elif value > self.critical:
			return "unhealthy"
		return "critical"

class INESubreddit:
	def __init__(self, reddit, name, tab="Unlisted"):
		'''
		Initialisation function
			
			@param
			-reddit: PRAW reddit instance we are using
			-name: name of the subreddit
			-tab: tab of this INE subreddit. Set to unlisted by default.
		'''
		self.__reddit = reddit
		self.name = name
		self.tab = tab
		
		self.__inst = None
		self.__var = None
		self.__submissions = list()

	def __repr__(self):
		'''
		Representation method
			
			@return
			Returns a string representation
		'''
		s = "INESubreddit("+str(self.__reddit)+","+self.name+","+self.tab+")"
		return s

	def pprint(self):
		'''
		A pretty print function
		'''
		s = "Subreddit: "+"/r/imaginary"+self.name+"\n"
		s += "\t"+"Tab: "+self.tab+"\n"
		s += "\t"+"Subscribers: "+str(self.get_subscribers())+"\n"
		return s
	
	def update(self, to_update="all", time_limit=30):
		'''
		Update this INESubreddit to set its variables to latest values.

		Instead of calling reddit every time, why not save all the data until
		we decide to update?
			
			@param
			-to_update: Which specific part you want to update
			-time_limit: how many submissions we want to

			@return
			Returns the time it took to complete the update
		'''
		start_time = time.time()

		if to_update == "all":
			self.__inst = self.__reddit.get_subreddit(str('imaginary'+self.name), fetch=True)
			self.__var = vars(self.__inst)
			self.__submissions = self.last_submissions(time_limit)
		elif to_update == "instance":
			self.__inst = self.__reddit.get_subreddit(str('imaginary'+self.name), fetch=True)
			self.__vars = vars(self.__inst)
		elif to_update == "submissions":
			self.__submissions = self.last_submissions(time_limit)

		# May be useless, but it's always good to have some debug data
		return time.time()-start_time
	
	def last_submissions(self, time_limit=30):
		submissions = self.get_inst().get_new(limit=100)
		filtered_submissions = []
		for s in submissions:
			v = vars(s)
			if time.time()-v["created_utc"] <= time_limit*24*60*60:
				filtered_submissions.append(s)
		return filtered_submissions


	def get_inst(self):
		'''
		Returns the subreddit instance associated with this INESubreddit
		'''
		return self.__inst
	
	def get_vars(self):
		'''
		Returns a dictionary representation of the subreddit instance
		'''
		return self.__var
	
	def get_subscribers(self):
		return self.__var["subscribers"]
	
	def get_time_filtered_submissions(self):
		return self.__submissions

	def get_submissions_health(self, threshold=HealthThreshold(15, 5),time_limit=30):
		'''
		Checks the health based on a HealthThreshold object
			
			@param
			-threshold: HealthThreshold object to use to check health
			
			@return
			Returns the health of this INESubreddit instance
		'''
		return threshold.rate_health(len(self.get_time_filtered_submissions()))

characters = [
	'archers',
	'assassins',
	'astronauts',
	'clerics',
	'cowboys',
	'fashion',
	'knights',
	'lovers',
	'natives',
	'ninjas',
	'nobles',
	'pirates',
	'soldiers',
	'vikings',
	'warriors',
	'witches',
	'wizards',
	'equestria',
	'westeros',
	'mindscapes',
	'jedi'
	]

def main():
	'''
	Main function
	'''
	r = praw.Reddit(user_agent="network_health")
	printer = Printer()

	output = ""
	count = 0
	
	for s in range(len(characters)):
		sub = INESubreddit(r, characters[s], "characters")
		update_time = sub.update("all",30)
		printer.append_csv("characters",characters[s],sub.get_subscribers(),sub.get_submissions_health(),len(sub.get_time_filtered_submissions()))
	
	output_file = open("output.csv","w")
	output_file.write(printer.output_csv())
	output_file.close()

main()
