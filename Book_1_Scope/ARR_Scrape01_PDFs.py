import requests
from bs4 import BeautifulSoup
import urllib

# Downloads PDFs (suffix) from URL to containing folder. Written in python27
bs = BeautifulSoup
#url = "http://www.arr-software.org/pdfs/"
url ="https://www.engineersaustralia.org.au/sites/default/files/shado/Learned%20Groups/National%20Committees%20and%20Panels/Water%20Engineering/k.heron_s.dooland_consideration_of_flood_events_during_construction.pdf"
suffix = ".pdf"
link_list = []

def getPDFs():    
    # Gets URL from user to scrape
    response = requests.get(url, stream=True, verify=False)
    soup = bs(response.text, "lxml")

    for link in soup.find_all('a'): # Finds all links
        if suffix in str(link): # If the link ends in .pdf
            link_list.append(link.get('href'))
    print(link_list)
    
    for link in link_list:
        urllib.urlretrieve(url+link, link)
        print ('downloading...'+link)

getPDFs()
