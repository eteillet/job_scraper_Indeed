import json
from bs4 import BeautifulSoup
import requests
import urllib
import re
import datetime
import os

RESULT_FILE_PATH='results.json'

def get_context(title, location):
    """
    - define the url we want to request (type of job, location ...)
    - get the html content of the page ready to parse
    """
    get_options = {'q' : title, 'l' : location}
    url = 'https://fr.indeed.com/emplois?' + urllib.parse.urlencode(get_options)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"})
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup

def get_title(job_elem):
    return job_elem.find('a', class_='jcs-JobTitle').text.strip()  

def get_company(job_elem):
    return job_elem.find(class_='companyName').text.strip()

def get_location(job_elem):
    return job_elem.find(class_='companyLocation').text.strip()

# on indeed, the dates are of type "il y a x jours", so we need to substract these days from today
def get_date(job_elem):
    """ on indeed, the dates are of type "il y a x jours", so we need to substract these days from today """
    date_elem = job_elem.find(class_='date').text.strip()
    numbers_in_job_elem = re.findall(r'-?\d+\.?\d*', str(date_elem))
    days_since_publication = 0
    if len(numbers_in_job_elem) == 1:
        days_since_publication = int(numbers_in_job_elem[0])
    days_to_substract = datetime.timedelta(days_since_publication)
    return str(datetime.date.today() - days_to_substract)

def get_url(job_elem):
    return 'https://fr.indeed.com' + job_elem.find('a')['href']

def extract_job_details(job, job_elem):
    job['title'] = get_title(job_elem)
    job['company'] = get_company(job_elem)
    job['location'] = get_location(job_elem)
    job['date'] = get_date(job_elem)
    job['url'] = get_url(job_elem)
    return job

def scrap_job_informations(soup):
    """ scraps informations for each job """
    data = []
    jobs = soup.find_all(class_=re.compile("cardOutline"))
    for elem in jobs:
        job = dict()
        job = extract_job_details(job, elem)
        data.append(job)
    return data

def scrap_indeed(titles, locations):
    data_collected = []
    for title in titles:
        for location in locations:
            soup = get_context(title, location)
            jobs = scrap_job_informations(soup)
            data_collected.append(jobs)
    with open('results.json', 'a') as fp:
        json.dump(data_collected, fp, sort_keys=False, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if os.path.isfile(RESULT_FILE_PATH):
        os.remove(RESULT_FILE_PATH)
    while True:
        titles_default = ["data scientist", "data analyst", "stage data"]
        titles = input(f"Jobs by default are : {titles_default}\n\t- If you want, you can search for other jobs (separated by a comma) else type Enter:\n\t>> ").split(",")
        if len(titles) == 1 and titles[0] == '':
            titles = titles_default
        locations_default = ["vendee", "loire-atlantique"]
        locations = input(f"Locations by default are : {locations_default}\n\t- If you want, you can search for other locations (separated by a comma) else type Enter:\n\t>> ").split(",")
        if len(locations) == 1 and locations[0] == '':
            locations = locations_default
        scrap_indeed(titles, locations)
        reset = input(f"- Do you want to reset the {RESULT_FILE_PATH} file ?  y/n\n\t>> ")
        if reset == 'y' and os.path.isfile(RESULT_FILE_PATH):
            os.remove(RESULT_FILE_PATH)
        quit = input("- Do you want to exit the program ?  y/n\n\t>> ")
        if quit == 'y':
            exit("Bye and good luck for your job search !")