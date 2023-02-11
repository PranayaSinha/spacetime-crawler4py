import re
from urllib.parse import urlparse
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link, resp)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content\

    links = []
    if(resp.status == 200):
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        with open("Text.txt", "a") as file:
            # Write the text to the file
            file.write(soup.getText())
        for link in soup.find_all('a'):
            link = link.get('href')
            if link:
                # Defragment the URL
                link = urlparse(link)._replace(fragment='').geturl()
                # Transform relative to absolute URL
                link = urljoin(url, link)
                links.append(link)
                print(link)
    return links

def is_valid(url, resp=""):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        if(resp != ""):
            # Detect if active
            if resp.status != 200:
                return False
            
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
            
            # Detect and avoid large files, especially if they have low information value
            if(len(str(soup))) > 15000:
                print(len(str(soup)))
                return False
            
            if(len(str(soup))) < 10:
                print(len(str(soup)))
                return False

            # Detect and avoid dead URLs that return a 200 status but no data
            if(len(str(soup))) == 0:
                print(len(str(soup)))
                return False

            # Detect and avoid sets of similar pages with no information

            # Detect and avoid infinite traps
        
        
        # Honor the politeness delay for each site
        time.sleep(1)

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
