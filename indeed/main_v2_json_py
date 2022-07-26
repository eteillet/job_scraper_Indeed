# goal :
#  - find companies that recruit data scientists in Nantes

from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib
import re
import datetime
import os

RESULT_FILE_PATH='results.xlsx'

# we define the url we want to request (type of job, location ...)
# we define the element in html code we want (here the 'mosaic-zone-jobcards' id)
# get the html content of the page ready to parse
def get_context(title, location):
    get_options = {'q' : title, 'l' : location}
    url = 'https://fr.indeed.com/emplois?' + urllib.parse.urlencode(get_options)
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"}
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup
    

def scrap_job_informations(title, job_soup):
    # use of a regex to find all class containing "cardOutline"
    job_elems = job_soup.find_all(class_=re.compile("cardOutline"))
    cols = []
    extracted_info = []

    research = []
    cols.append('research')
    for job_elem in job_elems:
        research.append(title)
    extracted_info.append(research)

    titles = []
    cols.append('title')
    for job_elem in job_elems:
        titles.append(get_title(job_elem))
    extracted_info.append(titles)
    
    companies = []
    cols.append('company')
    for job_elem in job_elems:
        companies.append(get_company(job_elem))
    extracted_info.append(companies)

    locations = []
    cols.append('location')
    for job_elem in job_elems:
        locations.append(get_location(job_elem))
    extracted_info.append(locations)

    links = []
    cols.append('link')
    for job_elem in job_elems:
        links.append(get_link(job_elem))
    extracted_info.append(links)

    dates = []
    cols.append('date')
    for job_elem in job_elems:
        dates.append(get_date(job_elem))
    extracted_info.append(dates)

    jobs_list = {}
    for i in range(len(cols)):
        jobs_list[cols[i]] = extracted_info[i]

    return jobs_list

# extract titles
def get_title(job_elem):
    return job_elem.find('a', class_='jcs-JobTitle').text.strip()  

# extract company name
def get_company(job_elem):
    return job_elem.find(class_='companyName').text.strip()

# extract exact location
def get_location(job_elem):
    return job_elem.find(class_='companyLocation').text.strip()

# extract date
# on indeed, the dates are of type "il y a x jours", so we need to substract these days from today
def get_date(job_elem):
    date_elem = job_elem.find(class_='date').text.strip()
    numbers_in_job_elem = re.findall(r'-?\d+\.?\d*', str(date_elem))
    days_since_publication = 0
    if len(numbers_in_job_elem) == 1:
        days_since_publication = int(numbers_in_job_elem[0])
    days_to_substract = datetime.timedelta(days_since_publication)
    return datetime.date.today() - days_to_substract

def get_link(job_elem):
    return 'https://fr.indeed.com' + job_elem.find('a')['href']

# save to csv
def save_to_csv(jobs):
    j = pd.DataFrame(jobs)
    j.to_csv(RESULT_FILE_PATH, mode='a', index=False, header=not os.path.exists(RESULT_FILE_PATH))


def scrap_indeed(titles, locations):
    for title in titles:
        for location in locations:
            soup = get_context(title, location)
            print(title, location, type(soup))
            jobs = scrap_job_informations(title, soup)
            save_to_csv(jobs)

if __name__ == "__main__":
    while True:
        # titles = input("- Your dream jobs (separated by a comma) :\n\t>> ").split(",")
        titles = ["data scientist", "data analyst", "stage data"]
        # locations = input("- Your dream locations (separated by a comma) :\n\t>> ").split(",")
        locations = ["vendee", "loire-atlantique", "la rochelle", "niort"]
        scrap_indeed(titles, locations)
        reset = input("- Do you want to reset the results.csv file ?  y/n\n\t>> ")
        if reset == 'y' and os.path.isfile(RESULT_FILE_PATH):
            os.remove(RESULT_FILE_PATH)