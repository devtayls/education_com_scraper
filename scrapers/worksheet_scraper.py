import re
from scrapers.scraper import download_resource, get_url
from parser import make_soup

__image_directory__ = './downloads/worksheets/images'
__worksheet_directory = './downloads/worksheets/sheets'
__absolute_url__ = 'https://www.education.com'
__capture_failures__ = {}


def capture_failure(field):
    if field in __capture_failures__:
        __capture_failures__[field] += 1
    else:
        __capture_failures__[field] = 0

def get_iterable_elements(soup, text):
    elements = []

    try:
        iterable_section = soup.findChild('h5', text=text).next_sibling
        for i in iterable_section:
            elements.append(i.text)
    except:
        capture_failure(text)
    return elements

def scrape_worksheet(relative_url):

    worksheet_content = {}
    url = __absolute_url__ + relative_url

    worksheet_page = make_soup(url)

    worksheet_content['name'] = (re.findall('article\/(.+)\/', relative_url))[0]

    # grab the tag of primary main content of this worksheet
    worksheet_module_content = worksheet_page.findChildren('div', re.compile('worksheet-module_content_'))  # the main worksheet module

    try:
        # download the associated image
        image_tag = (worksheet_module_content[0].findChildren('img'))[0]  # the image of the worksheet
        file_format = (re.findall('/\d+\/.*\.(\w*)', image_tag['src']))[0]
        download_resource(image_tag['src'], __image_directory__, worksheet_content['name'], file_format)
    except:
        capture_failure('image_meta')

    try:
        # the written description of the worksheet
        worksheet_content['description'] = str(worksheet_module_content[0].findChild('p').contents)
    except:
        capture_failure('description')

    try:
        worksheet_tag = (worksheet_module_content[0].findChildren('a', re.compile('worksheet-module_mainActionButton_')))[0]
        file_format = (re.findall('/\d+\/.*\.(\w*)', worksheet_tag['href']))[0]
        # TODO: This should work but I need a subscription first
        # download_resource(worksheet_tag['href'], __worksheet_directory, worksheet_content['name'], file_format)
        worksheet_content['worksheet_file_format'] = file_format
        worksheet_content['original_download_link'] = worksheet_tag['href']
    except:
        capture_failure('worksheet_meta')

    try:
        # TODO: this fails sometimes. Do I care enough to fix it?
        #  related worksheet set e.g., trace the letters set
        worksheet_set_tag = (worksheet_module_content[0].findChild('a', re.compile('Action-module_action')))  # set link
        if worksheet_set_tag is not None:
            if worksheet_set_tag.has_attr('href'):
                worksheet_content['set_link'] = worksheet_set_tag['href']
            if worksheet_set_tag.has_attr('title'):
                worksheet_content['set_title'] = worksheet_set_tag['title']
    except:
        capture_failure('set_meta')

    worksheet_content['grade_levels'] = get_iterable_elements(worksheet_page, 'Grade')
    worksheet_content['grade_levels'] = get_iterable_elements(worksheet_page, 'Grade')

    # TODO this breaks often. Do I care enough to fix it?
    # grab the link to the related guided lesson module
    try:
        guided_lesson = []

        related_guided_lesson_module = worksheet_page.findChildren('div', re.compile('RelatedGuidedLesson-module_container'))[0]

        if related_guided_lesson_module is not None:
            guided_lesson['title'] = related_guided_lesson_module.findChild('h3', re.compile('RelatedGuidedLesson-module_lessonTitle_')).text
            guided_lesson['download_link'] = related_guided_lesson_module.findChild('div', re.compile('RelatedGuidedLesson-module_downloadPrintables_')).contents[0]['href']
            worksheet_content['guided_lesson_module'] = guided_lesson
    except:
        capture_failure('guided_lesson_meta')

    # TODO remove debug statement
    print(worksheet_content)

    return worksheet_content




