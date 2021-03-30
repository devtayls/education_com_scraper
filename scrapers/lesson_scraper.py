import re
from scrapers.scraper import download_resource, get_url
from parser import make_soup

__image_directory__ = './downloads/lessons/images'
__worksheet_directory = './downloads/lessons/sheets'


def get_iterable_elements(soup, selector):
    elements = []

    try:
        iterable_section = soup.findChild('div', selector)

        for i in iterable_section:
            if hasattr(i, 'text'):
                elements.append(i.text)
    except:
        pass
    return elements


def scrape_lesson_plan(relative_url):
    lesson_plan = {}

    page = make_soup(get_url(relative_url=relative_url))

    # TODO think this might be broken
    lesson_plan['name'] = (re.findall('lesson-plan\/(.+)\/', relative_url))[0]
    lesson_plan['grade_levels'] = get_iterable_elements(page, 'Grade')
    lesson_plan['subject_matter'] = get_iterable_elements(page, 'Subject')

    lesson_plan['attachments'] = []
    attachments = page.findChildren('a', ['href', re.compile('attachment')])
    for i in attachments:
        attachment = {'label': i['href'], 'href': i['aria-label']}
        lesson_plan['attachments'].append(attachment)

    lesson_plan['learning_objectives'] = ((page.findChild('h4', text='Learning Objectives')).find_next('p')).contents[0]

    return lesson_plan

scrape_lesson_plan('/lesson-plan/living-and-nonliving-things/')
