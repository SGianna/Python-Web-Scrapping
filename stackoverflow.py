import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div",{"class":"s-pagination"})

    if pages: 
        pages = pages.find_all("a")
        last_page = pages[-2].get_text(strip=True)
    else:
        last_page = 0
        
    return int(last_page)

def extract_job_information(html):
    title = html.find("h2",{"class" : "mb4 fc-black-800 fs-body3"}).find("a")["title"]

    company, location = html.find("h3",{"class" : "fc-black-700 fs-body1 mb4"}).find_all("span", recursive = False)

    company = company.get_text(strip = True)
    location = location.get_text(strip = True)

    job_id = html.find("div",{"class":"flex--item d-flex ai-center w12"}).find("button")["data-id"]
    
    return {"title":title, "company":company , "location" : location, "link" : f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping stackoverflow page {page}")
        result = requests.get(f"{url}&pg={page+1}")        
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"-job"})

        for result in results:
            job = extract_job_information(result)
            jobs.append(job)

    return jobs
            
def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page,url)
    return jobs