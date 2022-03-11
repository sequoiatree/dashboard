'''...'''

import datetime
import regex as re
from typing import *

import pandas as pd

from . import constants
from . import enums
from . import io


def budget_status(
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


def register_regex(
    io_manager: io.IOManager,
    pattern: str,
    alias: Optional[str],
) -> None:
    '''...

    Args:
        pattern:
        alias:

    Returns:
        None.
    '''

    pattern = f'^{pattern}$'
    if not is_valid_regex(pattern):
        return

    def update_aliases(
        aliases: Dict[str, str],
    ) -> Dict[str, str]:
        '''...'''

        aliases.update({pattern: alias and alias.upper()})
        return aliases

    io_manager.update(enums.Data.aliases, update_aliases)


def register_tag_update(
    io_manager: io.IOManager,
    serialized_datum: Dict[str, str],
    new_tag: str,
) -> None:
    '''...

    Args:
        serialized_datum:
        new_tag:

    Returns:
        None.
    '''

    def update_saved_tags(
        saved_tags: pd.DataFrame,
    ) -> pd.DataFrame:
        '''...'''

        year = datetime.date.today().year
        date = datetime.datetime.strptime(serialized_datum['date'], '%a, %b. %d')
        datum = pd.DataFrame(
            {
                'account': serialized_datum['account'],
                'date': pd.Timestamp(datetime.date(year, date.month, date.day)),
                'amount': float(serialized_datum['amount']),
                'description': serialized_datum['description'],
                'tag': new_tag,
            },
            index=[0],
        )

        saved_tags_to_keep = (
            saved_tags
            .merge(datum.drop('tag', axis=1), how='outer', indicator=True)
            .loc[lambda union: union['_merge'] == 'left_only']
            .drop('_merge', axis=1)
        )

        return (
            saved_tags_to_keep
            .append(datum)
            .reset_index(drop=True)
        )

    io_manager.update(
        enums.Data.saved_tags,
        update_saved_tags,
        load_options=dict(
            columns=constants.SAVED_TAGS_COLUMNS,
        ),
    )


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
