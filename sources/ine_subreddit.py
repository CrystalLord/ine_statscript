#
# Filename: ine_subreddit.py
#
# Author: /u/CrystalLord
#
#

import praw
import time

SECONDS_PER_DAY = 86400

from health_threshold import *

class INESubreddit:
    def __init__(self, reddit, subreddit, tab="Unlisted"):
        '''
        Initialisation function
            
            @param
            -reddit: PRAW reddit instance we are using
            -name: name of the subreddit
            -tab: tab of this INE subreddit. Set to unlisted by default.
        '''
        self.name = subreddit.display_name
        self.tab = tab
        self.reddit = reddit
        
        self.inst = subreddit
        self.submissions = list()
        self.mod_submissions = list()

    def __repr__(self):
        '''
        Representation method
            
            @return
            Returns a string representation
        '''
        s = "INESubreddit("+str(self.subreddit)+","+self.name+","+self.tab+")"
        return s

    def pprint(self):
        '''
        A pretty print function
        '''

        s = "Subreddit: "+self.name+"\n"
        s += "\t"+"Tab: "+self.tab+"\n"
        s += "\t"+"Subscribers: "+str(self.get_subscribers())+"\n"
        return s
    
    def update(self, to_update="all", mods=[], time_limit=30):
        '''
        Update this INESubreddit to set its variables to latest values.

        Instead of calling reddit every time, why not save all the data until
        we decide to update?
            
            @param
            -mods: mod list to check if who are our mods.
            -to_update: Which specific part you want to update
            -time_limit: how many submissions we want to

            @return
            Returns the time it took to complete the update
        '''
        start_time = time.time()

        if to_update == "all":
            self.inst = self.reddit.subreddit(self.name)
            self.submissions = self.last_submissions(time_limit)
            self.mod_submissions = self.get_mod_posts(mods)
        elif to_update == "instance":
            self.inst = self.reddit.subreddit(self.name)
        elif to_update == "submissions":
            self.submissions = self.last_submissions(time_limit)
            self.mod_submissions = self.get_mod_posts(mods)

        # May be useless, but it's always good to have some debug data
        return time.time()-start_time
    
    def last_submissions(self, time_limit=30, post_limit=75):
        '''
        A costly function, gets the latest submitions based on a time limit

            @param
            -time_limit: number of days ago to search for old posts
            -post_limit: maximum number of posts to check until we recheck the
                subreddit. This is to prevent overchecking inactive subreddits.

            @return
            Returns a list of filtered submission classes
        '''
        submissions = self.inst.new(limit=post_limit)
        
        filtered_submissions = []
        
        # Since submissions is a generator, we can't do list comprehensions
        # with it.
        for s in submissions:
            v = vars(s)
            # Only count posts posted within the last time limit
            if time.time()-v["created_utc"] <= time_limit * SECONDS_PER_DAY:
                filtered_submissions.append(s)
        
        if len(filtered_submissions) >= post_limit:
            filtered_submissions = self.last_submissions(time_limit,
                post_limit * 2)
    
        return filtered_submissions
        
    def get_subscribers(self):
        return self.inst.subscribers
    
    def get_submissions_health(self, threshold=HealthThreshold(15, 5),
        time_limit=30):
        '''
        Checks the health based on a HealthThreshold object
            
            @param
            -threshold: HealthThreshold object to use to check health
            
            @return
            Returns the health of this INESubreddit instance
        '''
        return threshold.rate_health(len(self.submissions))

    def get_mod_posts(self, mods, nonmod=False):
        '''
        Returns a list of modposts, unless nonmod is set to True.
        Then it returns the posts that mods *didn't* make.
        
            @param
            -mods: The mods you want to check against. Need not be this
            subreddit's mods.
            -nonmods: A boolean value telling whether to return mod or nonmod
            submissions.

            @return
            Returns a list of submissions made or not made by mods
        '''
        mod_usernames = [x.name for x in mods]
        post_cache = []
        for submission in self.submissions:
            try:    
                # Is the author's username part of mods?
                if (submission.author.name in mod_usernames) and not nonmod:
                    # append the mod post
                    post_cache.append(submission)
                elif (not submission.author.name in mod_usernames) and nonmod:
                    # append the nonmod post
                    post_cache.append(suubmission)
            except AttributeError:
                # We hit a post with a deleted author: continue
                continue

        return post_cache
