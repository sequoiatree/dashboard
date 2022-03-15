'''Utilities.'''

import datetime
import regex as re
from typing import *


def error_message(
    *message: str,
    **macros: Any,
) -> str:
    '''Generate an error message from the given message strings and macros.

    For example:
    >>> x = 10
    >>> error_message(
    ...     'You entered the value {value} of type {type}.',
    ...     'Please try again.',
    ...     value=x,
    ...     type=type(x),
    ... )
    "You entered the value `10` of type `<class 'int'>`. Please try again."
    '''

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
    '''Determines whether the given string a valid RegEx pattern.'''

    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def months_ago(
    months_ago: int,
) -> int:
    '''Gets the month number corresponding to the requested month.

    Args:
        months_ago: The month number, 1-indexed for consistency with the
            `datetime` module.

    Returns:
        The 1-indexed month number corresponding to the month that occurred
        `months_ago` months ago. For example `months_ago=2` specifies 10
        (October) if called in December, but it specifies 12 (December) if
        called in February.
    '''

    curr_month = datetime.date.today().month
    prev_month = (curr_month - 1 - months_ago) % 12 + 1

    return prev_month
