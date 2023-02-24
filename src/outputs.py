import logging
import csv
import datetime as dt

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, FILE, RESULTS, PRETTY


LOG_INFO = 'Файл с результатами был сохранён: {name}'


def control_output(results, cli_args, *args):
    OUT[cli_args.output](results, cli_args)


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    dialects = csv.unix_dialect
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect=dialects)
        writer.writerows(results)
    logging.info(LOG_INFO.format(name=file_name))


OUT = {
    PRETTY: pretty_output,
    FILE: file_output,
    None: default_output
}
