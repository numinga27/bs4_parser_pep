import logging
import csv
import datetime as dt

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, RESULTS, utf


log_info = 'Файл с результатами был сохранён:'


def control_output(results, cli_args, *args):
    OUT = {
        'pretty': pretty_output,
        'file': file_output,
        None: default_output
    }
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
    dialects = csv.list_dialects()
    with open(file_path, 'w', encoding=utf) as f:
        writer = csv.writer(f, dialect=dialects)
        writer.writerows(results)
    logging.info('{0} {1}'.format(log_info, f'{file_name}'))
