from bs4 import BeautifulSoup
from time import sleep
import urllib.request
import pandas as pd
import requests
import urllib
import base64
import csv
import time


# Get site
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    
#page = driver.page_source
page = "https://unsplash.com/"
r = requests.get(page)
soup = BeautifulSoup(r.text, "html.parser")
# Gets srcs from all <img> from site 
srcs = [img['src'] for img in soup.findAll('img')]

# BELOW code = Writer writes all urls WITH comma after them

print ('Downloading URLs to file')
sleep(1)
with open('output.csv', 'w', newline='\n', encoding='utf-8') as csvfile:
#    writer = csv.writer(csvfile)
    for i,s in enumerate(srcs):  # each image number and URL
       csvfile.write(str(i) +','+s+'\n')

# Below is the code that only downloads the image from the first url. I intend for the code to download all images from all urls

print ('Downloading images to folder')
sleep(1)

filename = "output"

with open("{0}.csv".format(filename), 'r') as csvfile:
    # iterate on all lines
    i = 0
    for line in csvfile:
        splitted_line = line.split(',')
        # check if we have an image URL
        if splitted_line[1] != '' and splitted_line[1] != "\n":
            urllib.request.urlretrieve(splitted_line[1], "img_" + str(i) + ".png")
            print ("Image saved for {0}".format(splitted_line[0]))
            i += 1
        else:
            print ("No result for {0}".format(splitted_line[0]))
