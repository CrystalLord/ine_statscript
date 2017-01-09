#
# Filename: data_rake.py
#
# Author: CrystalLord
#

import time
import praw
import prawcore
import sys
import datetime

from tab_list import TabList
from csv_printer import CSVPrinter
from ine_subreddit import INESubreddit
from health_threshold import HealthThreshold

def data_rake(printer, moderator_centre, tabs, use_loading_bar=True):
    '''
        Rakes data from reddit, 
    '''
    
    # Load secret from external file
    # The secret file contains the user agent code and the client code
    # both of which are needed for reddit's OAuth2 system
    secret_file = open("client_secret", "r")
    client_id_code = secret_file.readline().rstrip()
    client_secret_code = secret_file.readline().rstrip()
    secret_file.close()

    # Setup PRAW
    r = praw.Reddit(client_id = client_id_code,
                client_secret = client_secret_code,
                user_agent = "Imaginary_Network_Expanded_Health_Script")

    # Get a list of all the Imaginary Network Expanded mods
    ine_mods = []
    for mod in r.subreddit(moderator_centre).moderator():
        ine_mods.append(mod)

    # List with elements of type TabList
    # We use this to iterate through to get the total number of subreddits
    tab_lists = []

    sys.stdout.write("Getting Tabs...")
    for tab in tabs:
        tab_lists.append(TabList(tab, get_tab_list(r, tab)))
        sys.stdout.write(".")
    sys.stdout.write('\n')

    # Number of total HTTP requests we need to send to Reddit
    total_required_requests = 0
    for tab_list in tab_lists:
        total_required_requests += tab_list.size
    
    # Print some useful information to know what's happening behind the scenes
    print("Total subreddits: " + str(total_required_requests))
    print("--Data collection: ")
    
    # Check to make sure we are have contacted reddit at least once
    if total_required_requests <= 0:
        print("Error: No subreddits found.")
        return
    
    requests_count = 0 # Request counter
    
    collected_data = []
    
    for tab_list in tab_lists:
        for s in range(len(tab_list.listings)):
            if use_loading_bar:
                update_loading_bar(requests_count/(total_required_requests-1))
            try:
                if not use_loading_bar:
                    print("    Getting "+tab_list.listings[s].display_name
                        +" data...")
                sub = INESubreddit(r,tab_list.listings[s], tab)
                update_time = sub.update(to_update="all",
                    mods=ine_mods, time_limit=30)
                
                if sub.get_subscribers() > 0:
                    post_sub_ratio = round((len(sub.submissions)
                        /sub.get_subscribers())*1000)/1000
                else:
                    post_sub_ratio = -1

                if len(sub.submissions) > 0:
                    percent_mods = round((len(sub.mod_submissions)
                        /len(sub.submissions))*1000)/1000
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
            except(prawcore.exceptions.Forbidden):
                # It's a forbidden subreddit, display an error and move on
                if not use_loading_bar:    
                    print("Error: "+tab_list.listings[s].display_name
                        +" forbidden. Continuing...")
                
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
            except(prawcore.exceptions.NotFound):
                # We couldn't find the subreddit, display an error and move on
                if not use_loading_bar:    
                    print("Error: "+tab_list.listings[s].display_name
                        +" is not found. Continuing...")
                
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
            #except Exception as ex:
                # Gracefully catch all data in case of any uncaught error
                # Or well, it's not very graceful yet...
            #    print("Error: uncaught exception: " + str(type(ex)))
            #    if not DRY_RUN:    
            #        print("Not Dry Run: Halting and writing output.")
            #        write_output(printer.output_csv())
            #    return

            requests_count += 1 # We made a request! Incremement the counter

    # Add a newline
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
    
    #TODO: Fix this monstrosity (see below fix commented out)
    ranked_data = [
        ranking_helper(
            collected_data[i],
            sorted_data.index(collected_data[i])+1
        ) for i in range(len(sorted_data))]
    
    #for i in range(len(sorted_data)):
    #    ranked_data.append(ranking_helper(collected_data[i],
    #        sorted_data.index(collected_data[i]+1)))

    for value in ranked_data:
        printer.append_csv(value)

#-------------------------------------------------------------------------------

def get_tab_list(reddit,tab):
    '''
        Generates a sorted list of all the subs in the tab of 
        /u/ImaginaryMod

        @param
        -tab: Imaginary Network tab to get subreddits from

        @return
        Returns the subreddits under a certain INE tab,
    '''
    multireddit = reddit.multireddit('imaginarymod', 'im'+tab)
    subs = multireddit.subreddits
    subs.sort(key = lambda j:j.display_name)
    return subs

def update_loading_bar(percentage):
    out = "Fetching: ["+str(round(percentage*100))+"%]"
    sys.stdout.write("\r"+out)
    sys.stdout.flush()

