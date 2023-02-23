from bs4 import BeautifulSoup

from exceptions import ParserFindTagException, ParserFindUrlException


LOAD_ERROR = 'Возникла ошибка при загрузке страницы {url}'
ERROR_TAG = 'Не найден тег {tag} {attrs}'
XML = 'lxml'


def get_response(session, url=None):
    response = session.get(url)
    if response is None:
        raise ParserFindUrlException(
            LOAD_ERROR.format(url=url),
            stack_info=True
        )
    response.encoding = 'utf-8'

    return response


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(
            ERROR_TAG.format(tag=tag, attrs=attrs))

    return searched_tag


def get_soup(session, url):
    response = get_response(session, url)
    soup = BeautifulSoup(response.text, features=XML)

    return soup
