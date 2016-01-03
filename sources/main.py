#
# Filename: main.py
#
# Authors:
# -/u/CVance1
# -/u/CrystalLord
#

import time
import praw
import sys
import datetime

from csv_printer import *
from ine_subreddit import *
from health_threshold import *

DRY_RUN = False

TABS = [
	'characters',
	'races',
	'landscapes',
	'nature',
	'architecture',
	'monsters',
	'technology',
	'fandoms',
	'nsfw',
	'meta'
	]

OUTPUT_NAME = "output.csv"
CENTRE = "ImaginaryNetwork"

USE_LOADING_BAR = True
LOADING_BAR_SIZE = 50

class Tab_List:
	def __init__(self, name, listings):
		self.name = name
		self.listings = listings
		self.size = len(listings)

#==========================================================================
# BEGIN MAIN
#==========================================================================

def main():
	'''
	Main function
	'''

	start_time = time.time() # start measuring the time
	r = praw.Reddit(user_agent="Imaginary_Network_Expanded_Health_Script")
	
	# Get a list of all the Imaginary Network Expanded mods
	ine_mods = r.get_moderators(r.get_subreddit(CENTRE))

	# Setup the printer
	printer = CSVPrinter()
	printer.set_timestamp(get_date_string())
	printer.set_header([
		'Tab',
		'Subreddit',
		'Rank',
		'Subscribers',
		'Submissions',
		'Health',
		'Posts/Subs',
		'% Mod',
		])
	
	output = ""
	count = 0
	
	# List with elements of type Tab_List
	# We use this to iterate through to get the total number of subreddits
	tab_lists = [] 
	
	print("Getting Tabs...")
	for tab in TABS:
		tab_lists.append(Tab_List(tab, get_tab_list(r, tab)))
	
	# Number of total HTTP requests we need to send to Reddit
	total_required_requests = 0
	for tab_list in tab_lists:
		total_required_requests += tab_list.size
	
	# Print some useful information to know what's happening behind the scenes
	print("Total subreddits: " + str(total_required_requests))
	print("--Data collection: ")
	
	# Check to make sure we are at least contact reddit at least once
	if total_required_requests <= 0:
		print("Error: No subreddits found.")
		return
	
	requests_count = 0 # Request counter
	
	collected_data = []

	for tab_list in tab_lists:
		for s in range(len(tab_list.listings)):
			if USE_LOADING_BAR:
				update_loading_bar(requests_count/(total_required_requests-1))
			try:
				if not USE_LOADING_BAR:
					print("    Getting "+tab_list.listings[s].display_name+" data...")
				sub = INESubreddit(r,tab_list.listings[s], tab)
				update_time = sub.update(to_update="all", mods=ine_mods, time_limit=30)
				
				if sub.get_subscribers() > 0:
				  	post_sub_ratio = round((len(sub.submissions)/sub.get_subscribers())*1000)/1000
				else:
				  	post_sub_ratio = -1

				if len(sub.submissions) > 0:
					percent_mods = round((len(sub.mod_submissions)/len(sub.submissions))*1000)/1000
				else:
					percent_mods = 0
				
				collected_data.append([
					tab_list.name,
					tab_list.listings[s].display_name,
					0, # Rank, not chosen yet
					sub.get_subscribers(),
					len(sub.submissions),
					sub.get_submissions_health(),
					post_sub_ratio,
					percent_mods,
					])
			except(praw.errors.Forbidden):
				# It's a forbidden subreddit, display an error and move on
				if not USE_LOADING_BAR:	
					print("Error: "+tab_list.listings[s].display_name+" forbidden. Continuing...")
				
				collected_data.append([
					tab_list.name,
					tab_list.listings[s].display_name,
					100000, # Rank
					0,
					"FORBIDDEN",
					"FORBIDDEN",
					"FORBIDDEN",
					"FORBIDDEN",
					])
			except(praw.errors.NotFound):
				# We couldn't find the subreddit, display an error and move on
				if not USE_LOADING_BAR:	
					print("Error: "+tab_list.listings[s].display_name+" is not found. Continuing...")
				
				collected_data.append([
					tab_list.name,
					tab_list.listings[s].display_name,
					100000, # Rank
					0,
					"NOT FOUND",
					"NOT FOUND",
					"NOT FOUND",
					"NOT FOUND",
					])
			except Exception as ex:
				# Gracefully catch all data in case of any uncaught error
				# Or well, it's not very graceful yet...
				print("Error: uncaught exception: " + str(type(ex)))
				if not DRY_RUN:	
					write_output(printer.output_csv())
				return

			requests_count += 1 # We made a request! Incremement the counter
	

	sys.stdout.write("\n")
	
	# Added in as of 2015-12-02:
	# Ranking of subreddits by subscriber count
	print("Getting subreddit rankings...")
	sorted_data = collected_data[:]
	sorted_data.sort(key=lambda r: r[3], reverse=True)
	
	def ranking_helper(element, r):
		new_element = element
		new_element[2] = r
		return new_element
	
	ranked_data = [ranking_helper(collected_data[i], sorted_data.index(collected_data[i])+1) for i in range(len(sorted_data))]
	
	for value in ranked_data:
		printer.append_csv(value)
	
	# print the data to csv file
	if not DRY_RUN:
		write_output(printer.output_csv())
		print("-------------------------")
		print("CSV printed to ../ine_logs/"+get_date_string()+"_"+OUTPUT_NAME)
		print("-------------------------")
	else:
		print("-------------------------")
		print("Dry run, no output printed")
		print("-------------------------")

	# Print out how long the entire process took
	print("Script completed in: "+str("%.3f" % (time.time()-start_time))+" seconds")

#==========================================================================
# END MAIN
#==========================================================================


def get_tab_list(reddit,tab):
    '''
    	Generates a sorted list of all the subs in the tab of 
	/u/ImaginaryMod

		@param
		-tab: Imaginary Network tab to get subreddits from

		@return
		Returns the subreddits under a certain INE tab,
    '''
    multireddit = reddit.get_multireddit('imaginarymod', 'im'+tab)
    subs=multireddit.subreddits
    subs.sort(key = lambda j:j.display_name)
    return subs

def write_output(out):
	# Write to csv file...
	output_file = open("../ine_logs/"+get_date_string()+"_"+OUTPUT_NAME,"w")
	output_file.write(out)
	output_file.close()

def update_loading_bar(percentage):
	out = "Fetching: ["+str(round(percentage*100))+"%]"
	sys.stdout.write("\r"+out)
	sys.stdout.flush()

def get_date_string():
	return datetime.datetime.utcnow().strftime("%Y-%m-%d")

# Main trick
if __name__ == "__main__":
	main()
