'''...'''

import datetime
import regex as re
from typing import *

import pandas as pd


def budget_status(  # TODO: Perhaps define this in the method where it's used. It doesn't belong in utils bc it's not generally useful.
    budget: float,
    spending: float,
) -> Tuple[float, str]:

    buffer = budget - abs(spending)
    status = 'OVER BUDGET' if buffer < 0 else 'WITHIN BUDGET'

    return buffer, status


def error_message(
    *message: str,
    **macros: Any,
) -> str:
    '''...'''

    return (
        ' '
        .join(message)
        .format(**{
            keyword: f'`{replacement}`'
            for keyword, replacement in macros.items()
        })
    )


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


def is_valid_regex(
    pattern: str,
) -> bool:
    '''...

    Args:
        pattern:

    Returns:
        ...
    '''

    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def months_ago(
    months_ago: int,
) -> int:
    '''... # 1-indexed (ie [1, 12]) to be consistent w datetime module

    Args:
        months_ago:

    Returns:
        ...
    '''

    curr_month = datetime.date.today().month
    prev_month = (curr_month - 1 - months_ago) % 12 + 1

    return prev_month


def stringify_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    '''...

    Args:
        df:

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
            raise TypeError(error_message(
                'Could not stringify column {name} with dtype {dtype}.',
                name=column.name,
                dtype=column.dtype,
            ))

    return df.apply(stringify_column)
