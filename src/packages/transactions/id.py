'''Account identification.'''

import regex as re
from typing import *

import pandas as pd

from . import enums
from . import utils


def identify_account(
    file: str,
    transactions: pd.DataFrame,
) -> enums.Account:
    '''Identifies the bank account associated with the given transaction data.'''

    if matches_ally(file, transactions):
        return enums.Account.ally
    elif matches_chase(file, transactions):
        return enums.Account.chase
    else:
        raise ValueError(utils.error_message(
            'Could not identify the account corresponding to {file}.',
            'You can implement the identification logic in {code}.',
            file=file,
            code=__file__,
        ))


def matches_ally(
    file: str,
    transactions: pd.DataFrame,
) -> bool:
    '''Determines whether the given transactions could be from Ally.'''

    columns = [
        'Date',
        ' Time',
        ' Amount',
        ' Type',
        ' Description',
    ]

    return (
        file == 'transactions.csv'
        and transactions.columns.to_list() == columns
    )


def matches_chase(
    file: str,
    transactions: pd.DataFrame,
) -> bool:
    '''Determines whether the given transactions could be from Chase.'''

    columns = [
        'Transaction Date',
        'Post Date',
        'Description',
        'Category',
        'Type',
        'Amount',
        'Memo',
    ]

    return (
        re.fullmatch(r'Chase\d{4}_Activity\d{8}_\d{8}_\d{8}.CSV', file)
        and transactions.columns.to_list() == columns
    )
