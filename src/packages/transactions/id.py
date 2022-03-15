'''Account identification.'''

import os
from typing import *

import pandas as pd

from . import constants
from . import enums
from . import utils


def identify_account(
    file: str,
    transactions: pd.DataFrame,
) -> enums.Account:
    '''Identifies the bank account associated with the given transaction data.'''

    if matches_ally(file, transactions):
        return enums.Account.ally
    # elif matches_____(file, transactions):
    #     return enums.Account.____
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
) -> pd.DataFrame:
    '''Determines whether the given transactions could be from Ally.'''

    columns = ['Date', ' Time', ' Amount', ' Type', ' Description']

    return (
        file == 'transactions.csv'
        and transactions.columns.to_list() == columns
    )
