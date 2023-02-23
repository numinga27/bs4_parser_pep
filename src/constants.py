from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'


BASE_DIR = Path(__file__).parent
DOWNLOADS = 'downloads'
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
RESULTS = 'results'
PRETTY = 'pretty'
FILE = 'file'


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
