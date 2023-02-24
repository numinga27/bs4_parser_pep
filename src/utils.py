from bs4 import BeautifulSoup

from exceptions import ParserFindTagException


LOAD_ERROR = 'Возникла ошибка при загрузке страницы {url}'
ERROR_TAG = 'Не найден тег {tag} {attrs}'
ENCODING = 'utf-8'


def get_response(session, url):
    response = session.get(url)
    if response is None:
        raise Exception(
            LOAD_ERROR.format(url=url)
        )
    response.encoding = ENCODING

    return response


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(
            ERROR_TAG.format(tag=tag, attrs=attrs))

    return searched_tag


def get_soup(session, url, XML='lxml'):
    response = get_response(session, url)
    soup = BeautifulSoup(response.text, features=XML)

    return soup
