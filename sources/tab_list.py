#
# Filename: tab_list.py
#
# Author: CrystalLord
# Creation Date: 2017-01-08
#

class TabList:
    def __init__(self, name, listings):
        '''
            Simple container class for subreddit list, organised by tab.
            -name: name of the tab
            -listings: list of subreddits names
        '''
        self.name = name
        self.listings = listings
        self.size = len(listings)
