# utils.py
import logging

from bs4 import BeautifulSoup

from exceptions import ParserFindTagException, ParserFindUrlException
from constants import utf


load_error = 'Возникла ошибка при загрузке страницы'
error_tag = 'Не найден тег'
error_soup = 'Страница не найдена'


def get_response(session, url):
    response = session.get(url)
    if response is None:
        raise ParserFindUrlException(logging.exception(
            f'{0} {1}'.format(load_error, f'{url}'),
            stack_info=True
        ))
    else:
        response.encoding = utf
        return response


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(
            '{0} {1} {2}'.format(error_tag, f'{tag}', f'{attrs}'))
    return searched_tag


def get_soup(session, url):
    response = get_response(session, url)
    if response is None:
        logging.error('{0} {1}'.format(error_soup, f'{url}'), stack_info=True)
        raise ParserFindUrlException(error_soup)
    soup = BeautifulSoup(response.text, features='lxml')

    return soup
