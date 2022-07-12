
from unittest import skip
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import requests

internal_urls = set()
not_found_urls = set()

total_urls_visited = 0
   
def Menu(option):
    
    
    option = input("Type Website url:");
    return option;


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that are found on `url` in which it belongs to the same website
    """

    urls = set()

    domain_name = urlparse(url).netloc

    try:
            soup = BeautifulSoup(requests.get(url).content, "html.parser")

    except (...):
        pass
    
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
        
            continue
        href = urljoin(url, href)

        parsed_href = urlparse(href)
        
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        
        
        if href in internal_urls:
            # already in the set
            continue

        
        if domain_name not in href:
           
            continue
        urls.add(href)
        internal_urls.add(href)
    return urls


def getLinks(url, max_urls=30):
    
    global total_urls_visited
    total_urls_visited += 1
    print(f"Crawling: {url}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        getLinks(link, max_urls=max_urls)
    


def crawl(url, max_urls=2000):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    checker = False
    

    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def print404Urls():

    urlcount = 0
    if not_found_urls != 0:
        for url in not_found_urls:

            
            urlcount+1
            print("404 Error: ", url)

        print(urlcount, " URLs were not found!")
    else:
        print("every URL was found! (no 404 Errors)")
         


def checkUrlFor404(urls):

    print("Checking For 404 Error...")
    for url in urls:
        
        

        try:
            r = requests.get(url)

            if(r.status_code == 404):

                not_found_urls.add(url)
        except(...):
            pass
        
    

    print404Urls()
if __name__ == "__main__":
    url = input("Please enter URL to check for 404 Error (not found):\n")
    print("Extracing Links...")
    crawl(url)

    print("[+] Total Internal links:", len(internal_urls)) 

    checkUrlFor404(internal_urls)
    
