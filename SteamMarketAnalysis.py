import requests
import urllib
import operator
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import brown
import numpy as np
import matplotlib.pyplot as plt
from numpy import arange
from matplotlib import pyplot
import xml.etree

# Dictionaries
topSellerTagDict = {}
upcomingTagDict = {}

def updateDict(dictType, data):
	if (dictType == "popularcomingsoon"):
		for index in range(len(data)):
			if data[index] in upcomingTagDict:
				upcomingTagDict[data[index]] += 1
			else:
				upcomingTagDict.update({data[index]: 1})
	elif (dictType == "topsellers"):
		for index in range(len(data)):
			if data[index] in topSellerTagDict:
				topSellerTagDict[data[index]] += 1
			else:
				topSellerTagDict.update({data[index]: 1})
	else:
		print("Invalid Dictionary")

def gameTagParser(dictType, url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "lxml")
	data = getattr(soup.find('div', {"class": "glance_tags popular_tags"}), "text", None)
	print(url)
	try:
		data = [x for x in re.split("\s{2,}", data) if x]
		updateDict(dictType, data)
	except TypeError:
		print("Type error")

def splitAtUpperCase(text):
	result = ""
	prevChar = ""
	for char in text:
		if char.isupper() and prevChar != '-' and prevChar != '2':#isinstance(prevChar, str):
			result += " " + char
		else:
			result += char
		prevChar = char
	return result.split()

# Parses both store pages for game urls
def gameParser(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "lxml")
	print(url)
	if "popularcomingsoon" in url:
		for data in soup.find_all('div', {"id": "search_resultsRows"}):
			for a in data.find_all('a'):
				gameTagParser("popularcomingsoon", a.get('href'))
				#print(a.get('href')) #for getting link
	elif "topsellers" in url:
		for data in soup.find_all('div', {"id": "search_resultsRows"}):
			for a in data.find_all('a'):
				gameTagParser("topsellers", a.get('href'))
				#print(a.get('href')) #for getting link
	else:
		print("Invalid store url.")

def executeParsers():

	# Parse store pages
	print("Popular Coming Soon...")
	gameParser("https://store.steampowered.com/search/?category1=998&os=win&filter=popularcomingsoon")
	print("Top Sellers")
	gameParser("https://store.steampowered.com/search/?category1=998&os=win&filter=topsellers")

	# Delete newline character
	del upcomingTagDict['+\n']
	del topSellerTagDict['+\n']

	# Sort dictionaries
	sortedUpcomingTagDict = dict( sorted(upcomingTagDict.items(), key=operator.itemgetter(1),reverse=True))
	sortedTopSellerTagDict = dict( sorted(topSellerTagDict.items(), key=operator.itemgetter(1),reverse=True))

	# Plot popular upcoming
	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	ax.bar(sortedUpcomingTagDict.keys(),sortedUpcomingTagDict.values())
	ax.plot()
	plt.suptitle('Popular Upcoming Genres')
	plt.xticks(rotation=90)
	plt.show()

	# Plot top sellers
	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	ax.bar(sortedTopSellerTagDict.keys(),sortedTopSellerTagDict.values())
	ax.plot()
	plt.suptitle('Top Seller Genres', fontsize=20)
	plt.xticks(rotation=90)
	plt.show()

#url = 'https://steamcdn-a.akamaihd.net/steam/apps/240/header.jpg?t=1602536047'
def iconDownload(dictType, url):
	# Icons
	r = requests.get(url, allow_redirects = True)
	imgName = url[url.find('=') + 1:]
	imgName = imgName + ".png"
	#urllib.request.urlretrieve(url, imgName)
	img_data = requests.get(url).content
	with open(imgName, 'wb') as handler:
	    handler.write(img_data)

def iconParser(dictType, url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "lxml")
	for data in soup.find_all('div', {"class": "game_header_image_ctn"}):
		for a in data.find_all('img'):
			iconDownload("download", a.get('src'))

# Parses both store pages for game urls
def gameIconParser(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "lxml")
	if "popularcomingsoon" in url:
		for data in soup.find_all('div', {"id": "search_resultsRows"}):
			for a in data.find_all('a'):
				iconParser("popularcomingsoon", a.get('href'))
	elif "topsellers" in url:
		for data in soup.find_all('div', {"id": "search_resultsRows"}):
			for a in data.find_all('a'):
				iconParser("topsellers", a.get('href'))
	else:
		print("Invalid store url.")

def main():
	#gameIconParser("https://store.steampowered.com/search/?category1=998&os=win&filter=popularcomingsoon")
	#gameIconParser("https://store.steampowered.com/search/?category1=998&os=win&filter=topsellers")

	executeParsers()

if __name__ == "__main__":
	main()


