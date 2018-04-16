#! /usr/bin/env python

# Extracts features from clickbait.csv dataset


import string
import pandas as pd
from nltk.corpus import stopwords

class FeatureExtraction:
	"""
	Class responsible for extracting features from clickbait and non-clickbait
	titles for model formation.
	"""

	def __init__(self, data):
		"""
		- Elements of intrigue (questions): Make a visualization
		- Elements of shock (cap letters per # of words, exclamations): Make a visualization/case study
		- Keywords (log ratio: Make a visualization
		"""
		self.data = data
		self.title = list(data['title'])
		self.clickbait = list(data['clickbait'])
		self.corpus = []
		self.corpus_clickbait = []
		self.caps_ratio = []
		self.exclamation = []
		self.question = []

	def get_corpus(self):
		"""
		Remove stopwords, remove punctuation, and lowercase (store in a new column)
		"""
		for title, clickbait in zip(self.title, self.clickbait):
			temp_np_title = title.strip(string.punctuation).split()
			np_title = [word.strip(string.punctuation) for word in temp_np_title]
			final_corpus = [word for word in np_title if word not in set(stopwords.words('english'))]
			self.corpus += [word.lower() for word in final_corpus]
			self.corpus_clickbait += [clickbait] * len(final_corpus)
		dataframe = pd.DataFrame({
			'corpus': self.corpus,
			'clickbait': self.corpus_clickbait})
		dataframe.to_excel('../data/corpus.xlsx', index = False)

	# Elements of Shock
	def get_caps_ratio(self):
		"""
		Get the ratio of capital letters per word in a title. 
		After an empirical observation of the clickbait and non-clickbait 
		titles, it appears that clickbait tiles have more capitalized letters
		"""
		for title in self.title:
			temp_np_title = title.strip(string.punctuation).split()
			np_title = [word.strip(string.punctuation) for word in temp_np_title]
			final_title = [word for word in np_title if word not in set(stopwords.words('english'))]
			final_title = " ".join(final_title)
			num_caps = len([elem for elem in final_title if elem.isupper()])
			num_words = len([elem for elem in final_title if elem == ' ']) + 1
			ratio = num_caps / num_words
			self.caps_ratio += [ratio]
		self.data['caps_ratio'] = self.caps_ratio

	def get_exclamations(self):
		"""
		Check if there are any exclamations in the title
		Exclamation attribute set to 0 by default.
		"""
		for title in self.title:
			if '!' in title:
				self.exclamation += [1]
			else:
				self.exclamation += [0]
		self.data['exclamation'] = self.exclamation

	# Elements of Intrigue
	def get_questions(self):
		"""
		Check if there are question keywords and a question mark in 
		"""
		question_kws = ['who', 'what', 'when', 'where', 'why', 'how', 'did']
		for title in self.title: 
			if '?' in title:
				self.question += [1]
			else:
				self.question += [0]
		self.data['question'] = self.question

	def export_data(self, filename):
		self.data.to_excel('../data/' + filename, index = False)

#------------------------------------RUN SCRIPT-----------------------------------------#

if __name__ == '__main__':
	data = pd.read_excel('../data/clickbait_data.xlsx')
	features = FeatureExtraction(data)
	features.get_corpus()
	features.get_caps_ratio()
	features.get_exclamations()
	features.get_questions()
	features.export_data('clickbait_final.xlsx')

