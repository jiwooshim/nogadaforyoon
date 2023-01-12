import requests
from bs4 import BeautifulSoup
from setlogging import logger
from utils import flatten_list


def get_links(URL):
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    main = soup.find_all('div', 'productThumb')
    if not main:
        return None

    category_links = []
    for cat in main:
        try:
            category_title = cat.find_parent().text
            href = cat.find_parent().get('href')
            category_links.append(href.strip())
        except:
            continue

    return category_links


def scraper(main_url):
    logger.info(f"Current URL: {main_url}")
    category_links = get_links(main_url)
    if category_links is None:
        return None

#    output_links = []
#    for item in category_links:
#        category_title = item['category_title']
#        sub_url = item['url']
#        if "/shop/" in sub_url:
#            continue
#        res_scraper = scraper(sub_url)
#        if res_scraper is None:
#            continue
#        output_links.append(res_scraper)

    output_links = []
    for sub_url in category_links:
        # category_title = item['category_title']
        # sub_url = item['url']
        if "/shop/" in sub_url:
            output_links.append(sub_url)
            continue
        res_scraper = scraper(sub_url)
        if res_scraper is not None:
            output_links.append(res_scraper)
    return output_links


def main():
    logger.info('=' * 65)
    logger.info(f"Retrieving all product links from Green Image Tech")
    URL = "https://www.greenimagetech.com/products/"
    all_links = scraper(URL)
    all_links = list(flatten_list(all_links))
    logger.info(f"Retrieved {len(all_links)} product links from Green Image Tech")
    return all_links


if __name__ == "__main__":
    all_links = main()
