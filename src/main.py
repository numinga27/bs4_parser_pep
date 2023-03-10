import logging
import re
import requests_cache

from tqdm import tqdm
from urllib.parse import urljoin

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS,
                       EXPECTED_STATUS, MAIN_DOC_URL, PEP_URL)
from collections import defaultdict
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_soup


LOAD_ERROR = 'Возникла ошибка при загрузке страницы {url}'
PARSER_START = 'Парсер запущен!'
PARSER_COMMANDS = 'Аргументы командной строки: {arguments}'
PARSER_END = 'Парсер завершил работу.'
ERROR_MASSEGE = 'Не найден тег {tag}'
DOWNED = 'Архив был загружен и сохранён:{archive}'
ERROR_STATUS = ('Несовпадающие статусы: \n'
                '{status}\n'
                'Статус в картрочке : {card_status}\n'
                'Ожидаемые статусы: {key_expected}')
WORK_PROGARM = 'Ошибка в вылполнеия кода основной программы: {exception}'


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    main_div = find_tag(soup,
                        'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={
        'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})
    result = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    load_errors = []
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        try:
            soup = get_soup(session, version_link)
        except ConnectionError:
            load_errors.append(LOAD_ERROR.format(url=version_link))
            continue
        h1 = find_tag(soup, 'h1')
        dl = soup.find('dl')
        dl_text = dl.text.replace('\n', ' ')
        result.append(
            (version_link, h1.text, dl_text)
        )
    for massege in load_errors:
        logging.warning(massege)

    return result


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = soup.find('div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise ParserFindTagException(ERROR_MASSEGE.format(tag=a_tags))
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    main_tag = soup.find('div', {'role': 'main'})
    table_tag = main_tag.find('table', {'class': 'docutils'})
    pdf_a4_tag = table_tag.find('a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR/DOWNLOADS
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNED.format(archive=archive_path))


def pep(session):
    what_new_url = urljoin(
        MAIN_DOC_URL, PEP_URL)
    soup = get_soup(session, what_new_url)
    main_table = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    div_with_table = find_tag(main_table, 'tbody')
    section_by_python = div_with_table.find_all(
        'tr')
    results = [('Статус', 'Количество')]
    status_sum = defaultdict(int)
    errors = []
    load_errors = []
    for section in tqdm(section_by_python):
        version_a_tag = find_tag(section, 'td')
        preview_status = version_a_tag.text[1:]
        a_tag = find_tag(section, 'a')
        href = a_tag['href']
        link = urljoin(what_new_url, href)
        try:
            soup = get_soup(session, link)
        except ConnectionError:
            load_errors.append(LOAD_ERROR.format(url=link))
            continue
        dt_tags = soup.find_all('dt')
        for dt_tag in dt_tags:
            if dt_tag.text != 'Status:':
                continue
            status = dt_tag.find_next_sibling().text
            status_sum[status] += 1
            if status not in EXPECTED_STATUS[preview_status]:
                errors.append(
                    ERROR_STATUS.format(
                        status=link,
                        card_status=status,
                        key_expected=EXPECTED_STATUS[preview_status]
                    )
                )
    errors.append(load_errors)
    for messages in errors:
        logging.warning(messages)
    for status in status_sum:
        results.append((status, status_sum[status]))
    results.append(('Total', sum(status_sum.values())))

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    try:
        configure_logging()
        logging.info(PARSER_START)
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(PARSER_COMMANDS.format(arguments=args))
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
        logging.info(PARSER_END)
    except Exception:
        logging.exception(WORK_PROGARM.format(
            exception=Exception), stack_info=True)


if __name__ == '__main__':
    main()
