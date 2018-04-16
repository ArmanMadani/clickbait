#! /usr/bin/env python

# Collects clickbait data from Reddit

# https://www.reddit.com/r/savedyouaclick serves as the best centralized 
# repository of clickbait examples. 

# https:/www.reddit.com/r/news serves as a great repository for non-clickbait
# titles (there are rules against Clickbait titles; though the titles themselves
# may be misleading)

import praw
import json
import requests
import pandas as pd

class RedditCollector: 
	"""
	Class responsible for making API calls to Reddit and collecting 
	data from /r/savedyouaclick and /r/news
	"""
	def __init__(self, subreddit_name, scope = 'all', limit = None, export = False):
		"""
		Class initializer
		"""
		self.subreddit = subreddit_name
		self.scope = scope # top all time, hour, year, day, month, and week are available
		self.limit = limit # Set to None to retrieve as many as possible (default = 100)
		self.auth = json.load(open('key.json'))
		self.Reddit = None
		self.data = None
		self.export = export

	def oauth(self): 
		"""
		Authenticate with Reddit using Oauth2 authentication
		"""
		try:
			reddit = praw.Reddit(
				client_id = self.auth['CLIENT_ID'],
				client_secret = self.auth['CLIENT_SECRET'],
				password = self.auth['PASSWORD'],
				user_agent = self.auth['USER_AGENT'],
				username = self.auth['USERNAME']
				)
		except: 
			return "Unable to authenticate with Reddit"
		return reddit

	def reddit_auth(self):
		"""
		Create and authenticate a Reddit object
		"""
		self.Reddit = self.oauth()

	def get_subreddit(self):
		"""
		Call the subreddit endpoint with appropriate parameters for 
		the scope of the results (and any limits)
		"""
		reddit = self.Reddit
		subreddit = self.subreddit
		scope = self.scope
		limit = self.limit 
		# The following returns a generator
		sub_generator = reddit.subreddit(subreddit).top(scope, limit = limit) 
		titles = []
		for submission in sub_generator:
			titles += [submission.title]
		self.data = titles

	def format_titles(self, delimiter):
		"""
		Fortunately, as a rule, all submissions to r/savedyouaclick, MUST have a 
		pipe-delimiter ('|') between the clickbait tile itself and the reasoning 
		for why the user considered it clickbait

		e.g. "Top 3 Things Supermodels do to stay healthy | 1. Eat Well, 
		2. Exercise, 3. Sleep 8 Hours a Day" 
		"""
		if self.subreddit == 'savedyouaclick':
			self.data = list(map(lambda x: x.split(delimiter)[0], self.data))

	def export_dataframe(self, dataframe, filename, sep = ','):
		"""
		Export dataframe to an Excel file
		"""
		dataframe.to_excel(filename, index = False) 

#------------------------------------RUN SCRIPT-----------------------------------------#

if __name__ == '__main__':
	clickbait_collector = RedditCollector(subreddit_name = 'savedyouaclick', export = True)
	nonclickbait_collector = RedditCollector(subreddit_name = 'news', export = True)
	collectors = [clickbait_collector, nonclickbait_collector]
	records = []
	for collector in collectors: 
		collector.oauth()
		collector.reddit_auth()
		collector.get_subreddit()
		collector.format_titles('|')
		if collector.subreddit == 'savedyouaclick':
			clickbait_indicator = [1] * len(collector.data)
		else: 
			clickbait_indicator = [0] * len(collector.data)
		records += list(zip(collector.data, clickbait_indicator))
		df = pd.DataFrame.from_records(records)
	if collector.export:
		collector.export_dataframe(df, '../data/clickbait_data.xlsx')
	print('Clickbait Data Collected!')


