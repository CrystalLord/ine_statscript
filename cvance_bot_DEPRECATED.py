import praw
import csv
import sys
tabs = ['architecture', 'characters', 'fandoms', 'landscapes',
        'monsters', 'nature', 'nsfw', 'races', 'technology']

user_agent = "Python Script: INE Health Check 1.0 by /u/CVance1"
r=praw.Reddit(user_agent=user_agent)
#DeviantART id: theartseer
#ArtStation: Devan Suber
#Friendly mod of: Assassins, Archers, Armor, Battlefields, Cyberpunk, Elves
#Gaming, Knights, Ladyboners, Natives, and Warriors!

def get_sub_list(section):
    #generates a sorted list of all the subs in a section
    multireddit=r.get_multireddit('imaginarymod', 'im'+section)
    subs=multireddit.subreddits
    subs.sort(key = lambda j:j.display_name[9])
    return subs

def check_5000(section):
    #sort subs over/under threshold
    subs=get_sub_list(section)
    under=list()
    over=list()
    for sub in subs:
        if sub.subscribers <= 5000:
            under.append(sub)
        else:
           over.append(sub)
    return under, over

def health(section):
    #actual health check, will only show info when it's done
    unhealthy=list() #<15 submissions in last month
    critical=list() #<= 5 submissions last month
    under, over = check_5000(section)
    healthy = list(over) #>= 15 submissions last month
    #assume /u/Lol33ta is the submitter for all posts, because she probably is
    for sub in under:
        global x
        x=list(sub.get_top_from_month(limit = 100))
        if len(x) < 15 and len(x) > 5:
            unhealthy.append(sub)
        elif len(x) <= 5:
            critical.append(sub)
        else:
            healthy.append(sub)
    healthy.sort(key = lambda i:i.display_name[9]) #for nice essentially alphabetic sorting

    print " Unhealthy:"
    for sub in unhealthy:
        print "   " + sub.display_name + " ("+ str(len(x))+ ")"
    print "    Total: " + str(len(unhealthy))
    print
    print " Critical:"
    for sub in critical:
        print "   "+ sub.display_name + " (" + str(len(x)) + ")"
    if len(critical) != 0:
        print
    print "    Total: " + str(len(critical)) + "\n" 
    print " Healthy: "
    for sub in healthy:
        print "   "+ sub.display_name + " (" + str(len(x)) + ")"
    print "    Total:" + str(len(healthy))
    print
    return unhealthy, critical, healthy
def run_check(tabs):
    #to make it look pretty
    for tab in tabs:
        print tab+": \n"
        health(tab)

def output_csv():
    pass

run_check(tabs)
