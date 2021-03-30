from parser import make_soup
from scrapers.scraper import get_url

def get_last_pagination_num(url):
    soup = make_soup(url)

    # grab all of the pagination a elements and grab the last in the list
    last_page = int((soup.select('a[title*="Page "]'))[-1].string)

    return last_page


def get_item_urls(content, selector, limit=0):
    item_urls = set()
    last_page_num = get_last_pagination_num(get_url(content=content))

    if limit > 0:
        last_page_num = limit

    # loop through all the available pages starting at the first pagination url
    end_range = last_page_num + 1
    for i in range(1, end_range):

        # todo debugging code:
        print('page ' + str(i) + ' of ' + str(last_page_num))

        soup = make_soup(get_url(content=content, query_string='?page=' + str(i)))

        # grab all links with the data-type worksheet
        work_sheet_links = soup.select(selector)

        for j in work_sheet_links:
            item_urls.add(j.attrs['href'])

    #todo debugging code:
    print(item_urls)

    return item_urls


