#
# Filename: main.py
#
# Authors:
# -/u/CVance1
# -/u/CrystalLord
#

import os
import time
import praw
import sys
import datetime

from csv_printer import CSVPrinter
from ine_subreddit import INESubreddit
from health_threshold import HealthThreshold
from data_rake import data_rake

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
CENTRE_SUBREDDIT = "ImaginaryNetwork"

USE_LOADING_BAR = True
LOADING_BAR_SIZE = 50

#==========================================================================
# BEGIN MAIN
#==========================================================================

def main():
    '''
    Main function
    '''

    start_time = time.time() # start measuring the time

    # Setup the printer
    printer = CSVPrinter()
    printer.set_timestamp(get_date_string(), 8)
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
    
    # Get the data
    data_rake(printer, CENTRE_SUBREDDIT, TABS, USE_LOADING_BAR)

    # Print the data to csv file
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
    print("Script completed in: "+str("%.3f" % (time.time()-start_time))
        +" seconds")

#==========================================================================
# END MAIN
#==========================================================================

def write_output(out):
    # Write to csv file...
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_file = open(script_dir+"/../ine_logs/"+get_date_string()
        +"_"+OUTPUT_NAME,"w")
    output_file.write(out)
    output_file.close()

def get_date_string():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d")

# Main trick
if __name__ == "__main__":
    main()
