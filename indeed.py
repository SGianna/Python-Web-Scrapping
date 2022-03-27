import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_page(url):
    result = requests.get(url)
    
    soup = BeautifulSoup(result.text, "html.parser")
    
    pagination = soup.find("div",{"class":"pagination"})

    if pagination:
        links = pagination.find_all('a')
        pages = []
        for link in links[:-1]:
            pages.append(int(link.string))
        
        max_page = pages[-1]
    else:
        max_page = 0
    return max_page
    
def extract_job_information(html) :

    title = html.find("span", title=True).string
    
    company = html.find("span",{"class":"companyName"})
    company_anchor = company.find("a")
    
    if company_anchor is not None:
        company = company_anchor.string
    else:
        company = company.string
    
    company = company.strip()

    location = html.find("div",{"class":"companyLocation"})
    if location.string is None:
        location = location.text
    else:
        location = location.string  

    job_id = html["data-jk"]
    
    return {'title' : title, 'company' : company, 'location' : location, 'link' : f"https://ca.indeed.com/viewjob?jk={job_id}&q=Python"}

    
def extract_jobs(url,last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping indeed page {page}")
        result = requests.get(f"{url}&start={last_page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("a",{"class":"fs-unmask"})
        for result in results:
            job = extract_job_information(result)
            jobs.append(job)       
    return jobs

def get_jobs(word):
    url = f"https://ca.indeed.com/jobs?q={word}&limit={LIMIT}"

    last_page = get_last_page(url)
    jobs = extract_jobs(url,last_page)
    return jobs