'''Encoders.'''

import json
from typing import *

import pandas as pd

from . import utils


class DataFrameJSONEncoder(json.JSONEncoder):
    '''Encodes JSON-like Python objects that may contain Pandas DataFrames.'''

    def default(
        self,
        object: Any,
    ) -> str:
        '''Encodes the given object as a JSON string.'''

        if isinstance(object, pd.DataFrame):
            return (
                object
                .pipe(stringify_columns)
                .to_dict(orient='records')
            )

        return super().default(object)


def format_date(
    date: pd.Timestamp,
) -> str:
    '''Converts the given date into a string like 'Thu, Feb. 17'.'''

    weekday = date.strftime('%a')
    month = date.strftime('%b')
    day = date.strftime('%d').lstrip('0').rjust(2)

    return f'{weekday}, {month}. {day}'


def stringify_columns(
    table: pd.DataFrame,
) -> pd.DataFrame:
    '''Stringifies and formats all the elements in the given DataFrame.'''

    def stringify_column(
        column: pd.Series,
    ) -> pd.Series:
        '''Stringifies and formats all the elements in the given Series.'''

        if pd.api.types.is_datetime64_dtype(column):
            return column.apply(format_date)
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
