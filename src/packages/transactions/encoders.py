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
                .pipe(stringify_columns)
                .to_dict(orient='records')
            )

        return super().default(object)


def formate_date(
    date: pd.Timestamp,
) -> str:
    '''...

    Args:
        date:

    Returns:
        ...
    '''

    weekday = date.strftime('%a')
    month = date.strftime('%b')
    day = date.strftime('%d').lstrip('0').rjust(2)

    return f'{weekday}, {month}. {day}'


def stringify_columns(
    table: pd.DataFrame,
) -> pd.DataFrame:
    '''...

    Args:
        table:

    Returns:
        ...

    Raises:
        ...
    '''

    def stringify_column(
        column: pd.Series,
    ) -> pd.Series:
        '''...'''

        if pd.api.types.is_datetime64_dtype(column):
            return column.apply(formate_date)
        elif pd.api.types.is_float_dtype(column):
            return column.apply('{:.2f}'.format)
        elif pd.api.types.is_string_dtype(column):
            return column
        else:
            raise TypeError(utils.error_message(
                'Could not stringify column {name} with dtype {dtype}.',
                name=column.name,
                dtype=column.dtype,
            ))

    return table.apply(stringify_column)