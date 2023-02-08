import time
import concurrent.futures
import pyuser_agent
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import tracemalloc

# init the colorama module

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and '.pdf' not in parsed.path

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    headers = {"User-Agent": pyuser_agent.UA().random}
    page = requests.get(url, "html.parser", headers = headers)

    soup = BeautifulSoup(page.content, "html.parser")

    for a_tag in soup.findAll("a", href = True):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue

        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)

        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = "https://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls, internal_urls, external_urls

# number of urls visited so far will be stored here
total_urls_visited = 0

# @profile
def crawl(url):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links, internal_urls, external_urls= get_all_website_links(url)
    return links, internal_urls, external_urls

# tracemalloc.start()
# s_time = time.time()
# if __name__ == "__main__":
#     main_page_links = crawl("https://nishkaloverseas.com/")
#     with concurrent.futures.ThreadPoolExecutor(5) as executor:
#         result = executor.map(crawl, main_page_links)
#
#     print("[+] Main Page links:", len(main_page_links))
#     print("[+] Total Internal links:", len(set(internal_urls)))
#     print("[+] Total External links:", len(set(external_urls)))
#     print("[+] Total URLs:", len(external_urls) + len(internal_urls))
#
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
# print(time.time() - s_time)
# tracemalloc.stop()
