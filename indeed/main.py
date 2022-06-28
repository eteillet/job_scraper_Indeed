# to start :
#  - python3 -m venv .venv
#  - python3 -m pip install beautifulsoup4
#  - python3 -m pip install requests
#  - python3 -m pip install lxml

# goal :
#  - find companies that recruit data scientists in Nantes

from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib

# we define the url we want to request (type of job, location ...)
# we define the element in html code we want (here the 'mosaic-zone-jobcards' id)
# get the html content of the page ready to parse
get_options = {'q' : 'data scientist', 'l' : 'Nantes', 'radius' : '25'}
url = 'https://fr.indeed.com/emplois?' + urllib.parse.urlencode(get_options)
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "html.parser")
jobs_soup = soup.find(id="resultsCol")
jobs_elem = jobs_soup.find_all('ul', class_='jobsearch-ResultsList')

cols = []
extracted_info = []


print(jobs_elem)

# extract titles
# def get_title(job):
#     title = job.find('h2', class_='title').text.strip()
#     print(title)
#     return title

# for job in jobs:
#     get_title(job)
# extract company name

# extract date

