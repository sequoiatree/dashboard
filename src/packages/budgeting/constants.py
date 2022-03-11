'''...'''

from typing import *

import numpy as np
import pandas as pd


JSON = Dict[str, Optional[Union[int, float, str, bool, List['JSON'], 'JSON']]]

TEMP_EXTENSION = '.tmp'

TRANSACTIONS_COLUMNS = {
    'account': pd.Series(dtype=np.dtype('str')),
    'date': pd.Series(dtype=np.dtype('datetime64[ns]')),
    'amount': pd.Series(dtype=np.dtype('float64')),
    'description': pd.Series(dtype=np.dtype('str')),
}

SAVED_TAGS_COLUMNS = {
    **TRANSACTIONS_COLUMNS,
    'tag': pd.Series(dtype=np.dtype('str')),
}
