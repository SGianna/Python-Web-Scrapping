import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://ca.indeed.com/jobs?q=Python&limit={LIMIT}"

def extract_indeed_pages():
    result = requests.get(URL)
    
    soup = BeautifulSoup(result.text, "html.parser")
    
    pagination = soup.find("div",{"class":"pagination"})
    
    links = pagination.find_all('a')
    
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    
    max_page = pages[-1]
    return max_page

def extract_indeed_jobs(last_page):
    jobs = []
    #for page in range(last_page):
    result = requests.get(f"{URL}&start={0*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a",{"class":"fs-unmask"})
    
    for result in results:
        jobTitle = result.find("h2", {"class": "jobTitle"})
        title = jobTitle.find("span").string
        if title == "new":
            title = jobTitle.find_all("span")[1].string
        print(title)
    return jobs