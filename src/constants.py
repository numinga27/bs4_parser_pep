from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP = 'https://peps.python.org/'


BASE_DIR = Path(__file__).parent
DOWNLOADS = 'downloads'
log_dir = BASE_DIR / 'logs'
log_file = log_dir / 'parser.log'
RESULTS = 'results'
utf = 'utf-8'


DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}


CHOICE_PRETTY = 'pretty'
CHOICE_FILE = 'file'
