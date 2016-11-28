#INE Health Stat Script
This script is for collecting data for the Imaginary Network Expanded to judge the health of its members.

##Planned Features
* [DONE!] ~~Percent mod posts~~
* [DONE!] ~~Change progress measurement into loading bar~~
* [DONE!] ~~Include a re-update for subs with >100 posts~~
* More detailed exception handling
* Better documentation
* [CANCELLED] ~~Read and update the CSV instead of rewriting it every time~~
* [DONE!] ~~Provide a month-by-month comparison~~
* Remove the auto-mod reliance (see `generalised` branch)

##Tutorial on how to use INE Statscript
As of this writing, INE Statscript is not packaged into an executable. This means it may require a prelimary setup step. Later versions may not need this step as a downloadable package may be available.

Please be aware: This script is NOT user friendly; it's more hostile than your mother-in-law. As such, it's still under semi-active development. Prod me more if you want it to be better, or fork it yourself!

###Setting up:

**Step 0 (ENVIRONEMT SETUP):**

Install any version of [Python 3](https://www.python.org/downloads/). It should work fine for 3.5, the current release. You also must have the [Python Reddit API Wrapper (PRAW)](https://praw.readthedocs.org/en/stable/) installed on your machine. PRAW can be installed via the `pip install praw` command, which makes it very easy to use. Please be aware that Python 2.7 or Python Anaconda probably will **NOT** work. You can check your Python3 version at any time using `python3 --version`. If you used pip to install PRAW, You can check your PRAW version by using `pip list`.

**Step 1:**

Ensure that [/u/ImaginaryMod](https://www.reddit.com/user/imaginarymod) is up to date with its public multireddits. If it's not up to date, the script will not gather the correct data, and will not provide the data you want.

**Step 2:**

If you know how to use git, clone the master branch of this repository on to your system. If you don't know how to use git, download the zip/tarball and open it into a directory of choice (download is on the right).

**Step 3:**

Make sure you have a reasonably stable internet connection. Currently the script does not recover properly when the internet cuts out, and the collection will be made invalid.

On completion of these 3 (or 4) steps, congratulations! You now have a working INE Statscript on your PC.

###How to use:

####Data Collection

Open the `/ine_statscript/sources` directory in terminal and run `python3 main.py`. If it stalls forever, it's because you probably ran `python main.py` instead. A loading screen will appear, it will take roughly 20 minutes to collect all the data. Once it is done, it should give a message that looks like this


	Getting Tabs...
	Total subreddits: ###
	--Data collection: 
	Fetching: [100%]
	Getting subreddit rankings...
	-------------------------
	CSV printed to ../ine_logs/YYYY-MM-DD_output.csv
	-------------------------
	Script completed in: ###### seconds

A new CSV file will appear in `/ine_statscript/ine_logs`. Be warned, running the script on the same day twice will overwrite the previous CSV file. If you want to keep several CSV files of the same day, rename the first version to something different.

CSV files can be opened in any spreadsheet program that's worth more than a roll of used toliet paper.

####Data comparison

Much like collection, open the `/ine_statscript/sources` directory in terminal and run `python3 compare.py`. A prompt should appear that looks like this

	Compare 2 INE matrices
	----------------------
	Filename of previous month matrix> 
	Filename of new month matrix> 

Fill in the prompts with the 2 file names of the CSV files located in `/ine_statscript/ine_logs` which you want to compare. It should complete in less than a second, and generate a CSV output now located in `/ine_statscript/ine_logs`.

##Questions
If you have any questions, PM me on reddit or leave an issue here.
