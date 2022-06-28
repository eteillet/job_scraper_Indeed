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

url = 'https://fr.indeed.com/jobs?q=data%20scientist&l=Nantes%20%2844%29&from=searchOnHP'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "lxml")

jobs = soup.find_all("ul", class_="jobsearch-ResultsList")
job_series = pd.Series(jobs)
job_series.value_counts()
# for job in jobs:
#     print("---------------\n")
#     print(job.get_text(strip=True))
