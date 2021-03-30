import wget

__absolute_url__ = 'https://www.education.com'


def download_resource(url, relative_path, file_name, file_format):
    print('in download_resource...')
    wget.download(url, relative_path + '/' + file_name + '.' + file_format)
    print('leaving download_resource')


def get_url(absolute_url=__absolute_url__, content='', section='', query_string='', relative_url=''):
    url = absolute_url
    if relative_url: url += relative_url
    if content: url += '/' + content
    if section: url += '/' + section
    if query_string: url += '/' + query_string

    return url
