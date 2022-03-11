'''...'''

import json
from typing import *

import pandas as pd

from . import utils


class DataFrameJSONEncoder(json.JSONEncoder):
    '''...'''

    def default(
        self,
        object: Any,
    ) -> str:
        '''...'''

        if isinstance(object, pd.DataFrame):
            return (
                object
                .pipe(utils.stringify_columns)  # TODO: Move stringify_columns here instead of utils.
                .to_dict(orient='records')
            )

        return super().default(object)
