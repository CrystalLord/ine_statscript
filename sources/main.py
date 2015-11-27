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

from csv_printer import *
from ine_subreddit import *
from health_threshold import *

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

def main():
	'''
	Main function
	'''
	start_time = time.time()
	r = praw.Reddit(user_agent="Imaginary_Network_Expanded_Health_Script")
	# Get a list of all the Imaginary Network Expanded mods
	ine_mods = r.get_moderators(r.get_subreddit(CENTRE))
	printer = CSVPrinter()
	printer.set_header([
		"Tab",
		"Subreddit",
		"Subscribers",
		"Submissions",
		"Health",
		"Posts/Subs",
		"% Mod",
		])

	output = ""
	count = 0
	
	for tab in TABS:
		tab_list = get_tab_list(r, tab)
		for s in range(len(tab_list)):
			try:
				print("Getting "+tab_list[s].display_name+" data...")
				sub = INESubreddit(r,tab_list[s], tab)
				update_time = sub.update(to_update="all", mods=ine_mods, time_limit=30)
				
				if sub.get_subscribers() > 0:
				  	post_sub_ratio = round((len(sub.submissions)/sub.get_subscribers())*1000)/1000
				else:
				  	post_sub_ratio = -1

				if len(sub.submissions) > 0:
					percent_mods = round((len(sub.mod_submissions)/len(sub.submissions))*1000)/1000
				else:
					percent_mods = 0

				printer.append_csv([
					tab,
					tab_list[s],
					sub.get_subscribers(),
					len(sub.submissions),
					sub.get_submissions_health(),
					post_sub_ratio,
					percent_mods,
					])
			except(praw.errors.Forbidden):
				# It's a forbidden subreddit, display an error and move on
				print("Error: "+tab_list[s].display_name+" forbidden. Continuing...")
				printer.append_csv([
					tab,
					tab_list[s],
					"FORBIDDEN",
					"FORBIDDEN",
					"FORBIDDEN",
					"FORBIDDEN",
					"FORBIDDEN",
					])
				continue
			except(praw.errors.NotFound):
				# We couldn't find the subreddit, display an error and move on
				print("Error: "+tab_list[s].display_name+" is not found. Continuing...")
				printer.append_csv([
					tab,
					tab_list[s],
					"NOT FOUND",
					"NOT FOUND",
					"NOT FOUND",
					"NOT FOUND",
					"NOT FOUND",
					])
			#except Exception as ex:
			#   # Gracefully catch all data in case of any uncaught error
			#	print("Error: uncaught exception: " + str(type(ex)))
			#	write_output(printer.output_csv())
			#	return
	
	# print the data to csv file
	write_output(printer.output_csv())
	print("-------------------------")
	print("CSV printed to "+OUTPUT_NAME)
	print("-------------------------")

	# Print out how long the entire process took
	print("Data collection duration: "+str("%.3f" % (time.time()-start_time))+" seconds")
	
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
	output_file = open(OUTPUT_NAME,"w")
	output_file.write(out)
	output_file.close()

if __name__ == "__main__":
	main()
