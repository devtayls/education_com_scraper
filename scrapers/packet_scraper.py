import re
from scrapers.scraper import download_resource, get_url
from parser import make_soup

__image_directory__ = './downloads/packets/images'
__worksheet_directory = './downloads/packets/sheets'


def get_packet_iterable_elements(soup, selector):
    elements = []

    try:
        iterable_section = soup.findChild('div', selector)

        for i in iterable_section:
            if hasattr(i, 'text'):
                elements.append(i.text)
    except:
        pass
    return elements


def scrape_workbook(relative_url):
    print(relative_url)

    packet = {}
    page = make_soup(get_url(relative_url=relative_url))

    try:
        packet['title'] = page.findChild('h1').text
    except:
        pass
    try:
        packet['description'] = (page.findChild('div', {'class' : 'description'})).text
    except:
        pass
    try:
        packet['download_link'] = page.findChild('a', {'class': 'download-link'})['href']
    except:
        pass
    packet['grade_levels'] = get_packet_iterable_elements(page, {'class': 'grades'})
    packet['subject_matter'] = get_packet_iterable_elements(page, {'class': 'subjects'})

    packet['image_link'] = page.findChild('img', {'class' : 'main-image'})['src']
    file_format = re.findall(".*\.(\S*)", packet['image_link'])[0]
    print('calling download_resource...')
    download_resource(url=packet['image_link'], relative_path='./downloads/packets/images', file_name='test', file_format='jpg')


    # todo debugging code
    print(packet)
    return packet

scrape_workbook('/workbook/independent-study-packet-kindergarten-week-5/')
