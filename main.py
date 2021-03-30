from database import insert_item
from worksheet_collector import get_item_urls

from scrapers.worksheet_scraper import scrape_worksheet
from scrapers.activity_scraper import scrape_activity
from scrapers.lesson_scraper import scrape_lesson_plan

def process_worksheets(save=True):
    # this grabs content from education.com/worksheets and uses that selector to grab the library of links
    item_urls = get_item_urls('worksheets', 'a[data-type="worksheet"]')

    # TODO remove debugging code
    iterator = 0
    for item in item_urls:
        scraped_worksheet = scrape_worksheet(item)

        if save is True:
            insert_item(scraped_worksheet)

        # TODO remove debugging code
        iterator += 1
        print(iterator)


def process_lesson_plans():

    item_urls = get_item_urls('lesson-plans', 'a[data-type="lesson-plans"]')

    for item in item_urls:
        scraped_lesson_plan = scrape_lesson_plan(item)
        insert_item(scraped_lesson_plan, 'lesson-plans')


def process_activities():
    item_urls = get_item_urls('activity', 'a[data-type="activity"]', 0)
    print(item_urls)
    num_items = len(item_urls)

    # TODO remove debugging code
    iterator = 0
    for item in item_urls:
        scraped_worksheet = scrape_activity(item)
        insert_item(scraped_worksheet, 'activities')
        iterator += 1
        print(str(iterator) + ' of ' + str(num_items) )

print('starting now...')
# process_worksheets()
process_activities()
# process_lesson_plans()

