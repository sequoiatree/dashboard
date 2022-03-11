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
