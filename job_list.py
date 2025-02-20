import requests
from bs4 import BeautifulSoup
import csv
import random
import time
import gzip
import brotli
from lxml import etree


URL = "https://ai-jobs.net/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

URL = "https://ai-jobs.net/"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
]

HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",  
    "DNT": "1", #(DNT means do not track)
    "Upgrade-Insecure-Requests": "1"
}

def fetch_jobs():
    try:
        response = requests.get(url=URL, headers=HEADERS)
        if response.status_code != 200:
            print(f" Failed to fetch jobs: {response.status_code}")
            return []
        #print(response.headers)

        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    #dom = etree.HTML(str(soup))
    #jobs = dom.xpath('//*[@id="job-list"]/li/div/a/h5')
    #for job in jobs:
     #   print(job.text)

    jobs = soup.find_all("a", class_='py-2')
    print("Jobs - List: \n", jobs)
    job_list = []
    for job in jobs:
        title = job.find('h5').text if job.find('h5') else "Found Nothing"
        dom = etree.HTML(str(job))
        location = job.find('div').find('span', class_='d-block').text #dom.xpath('//*[@id="job-list"]/li[1]/div/a/div/span[1]')
        company = job.find('span', class_='text-muted').text #dom.xpath('//*[@id="job-list"]/li[1]/div/a/span[1]')
        link = job.get('href') if job.get('href') else "Found Nothing"

        job_list.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Link": link
            })
    return job_list


def save_jobs_to_csv(jobs, filename='ai_jobs.csv'):
    if not jobs:
        print("NO JOBS FOUND")
        return []
    with open(filename, mode='w', newline = "", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Company", "Location", "Link"])
        writer.writeheader()
        writer.writerows(jobs)

        print(f"{len(jobs)} found and recorded")

def main():
        print('fetching job')
        html = fetch_jobs()
        jobs = parse_html(html)
        save_jobs_to_csv(jobs)

        
if __name__ == "__main__":
        time.sleep(random.uniform(2, 5))
        main()
    

                                
                     

x = parse_html(fetch_jobs())
print(x)





