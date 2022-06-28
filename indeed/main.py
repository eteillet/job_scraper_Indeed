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
import re
import datetime

# we define the url we want to request (type of job, location ...)
# we define the element in html code we want (here the 'mosaic-zone-jobcards' id)
# get the html content of the page ready to parse
get_options = {'q' : 'data scientist', 'l' : 'Nantes', 'radius' : '25'}
url = 'https://fr.indeed.com/emplois?' + urllib.parse.urlencode(get_options)
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "html.parser")
job_soup = soup.find(id="resultsCol")

# use of a regex to find all class containing "cardOutline"
job_elems = job_soup.find_all(class_=re.compile("cardOutline"))

cols = []
extracted_info = []

# extract titles
titles = []
cols.append('titles')
for job_elem in job_elems:
    title = job_elem.find('a', class_='jcs-JobTitle').text.strip()
    # print(title)
    titles.append(title)
extracted_info.append(titles)
print(len(titles), ' TITLES : ', titles)


# extract company name
companies = []
cols.append('companies')
for job_elem in job_elems:
    company = job_elem.find(class_='companyName').text.strip()
    companies.append(company)
extracted_info.append(companies)
print(len(companies), ' COMPANIES : ', companies)

# extract date
# on indeed, the dates are of type "il y a x jours", so we need to substract these days from today
dates = []
cols.append('date')
for job_elem in job_elems:
    date_elem = job_elem.find(class_='date').text.strip()
    days_since_publication = int(re.findall(r'-?\d+\.?\d*', str(date_elem))[0])
    days_to_substract = datetime.timedelta(days_since_publication)
    date_ = datetime.date.today() - days_to_substract
    # print(today, days_to_substract, date_)
    dates.append(date_)
extracted_info.append(dates)
print(len(dates), ' DATES : ', dates)
