'''Constants.'''

from typing import *


JSON = Dict[str, Optional[Union[int, float, str, bool, List['JSON'], 'JSON']]]

TRANSACTIONS_COLUMNS = {
    'account': 'string',
    'date': 'datetime64[ns]',
    'amount': 'float',
    'description': 'string',
}

SAVED_TAGS_COLUMNS = {
    **TRANSACTIONS_COLUMNS,
    'tag': 'string',
}
