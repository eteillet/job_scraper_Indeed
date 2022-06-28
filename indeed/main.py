# to start :
#  - python3 -m venv .venv
#  - python3 -m pip install beautifulsoup4

from bs4 import BeautifulSoup
import requests

url = 'https://fr.indeed.com/jobs?q=data%20scientist&l=Nantes%20(44)&vjk=1472d157bc99cfea'
soup_obj = BeautifulSoup(html_obj, 'html.parser')