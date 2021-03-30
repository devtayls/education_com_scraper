import re
from scrapers.scraper import download_resource, get_url
from parser import make_soup

__image_directory__ = './downloads/activities/images'
__worksheet_directory = './downloads/activities/sheets'
iterator_failed_subject = []

def get_activity_iterable_elements(soup, selector):
    elements = []

    try:
        iterable_section = soup.findChild('div', selector)

        for i in iterable_section:
            if hasattr(i, 'text'):
                elements.append(i.text)
    except:
        pass
    return elements


def scrape_activity(relative_url):
    print(relative_url)

    activity = {}
    page = make_soup(get_url(relative_url=relative_url))

    try:
        activity['title'] = page.findChild('h1').text
    except:
        pass
    try:
        activity['description'] = (page.findChild('div', {'class' : 'description'})).text
    except:
        pass
    try:
        activity['download_link'] = ((page.findChild('div', {'class' : 'main-actions'})).findChild('a'))['href']
    except:
        pass
    activity['grade_levels'] = get_activity_iterable_elements(page, {'class': 'grades'})
    activity['subject_matter'] = get_activity_iterable_elements(page, {'class': 'subjects'})
    try:
        activity['lesson_text'] = page.findChild('div', {'class' : 'bottom-text'}).text
    except:
        pass
    try:
        activity['image_link'] = page.findChild('img', {'class' : 'main-image'})['src']
        file_format = re.findall(".*\.(\S*)", activity['image_link'])[0]
        download_resource(activity['image_link'], __image_directory__, activity['title'], file_format)
    except:
        pass

    # todo debugging code
    print(activity)
    return activity
