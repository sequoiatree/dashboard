'''...'''

import os

import pandas as pd

from . import constants
from . import enums


def parse_transactions(
    upload_dir: str,
    file: str,
):
    '''...'''

    path = os.path.join(upload_dir, file)
    try:
        transactions = pd.read_csv(path, dtype='string')
    except Exception as exception:
        raise ValueError() from exception  # TODO - include a helpful error message

    account = identify_account(file, transactions)

    if account is enums.Account.ally:
        transactions = parse_transactions_from_ally(transactions)
    # elif account is enums.Account.____:
    #     transactions = parse_transactions_from_____(transactions)
    else:
        raise ValueError(...)  # TODO

    transactions = transactions.astype(constants.TRANSACTIONS_COLUMNS)

    return transactions


def identify_account(
    file: str,
    transactions: pd.DataFrame,
) -> enums.Account:
    '''...

    Args:
        file:
        transactions:

    Returns:
        ...

    Raises:
        ...
    '''

    # TODO: Maybe don't empty the uploads folder on app init. Instead just delete files that are successfully loaded into the Transactions object (but only delete after saving).

    if file == 'transactions.csv':
        return enums.Account.ally
    # elif ____:
    #     return enums.Account.____
    else:
        raise ValueError(...)  # TODO


def parse_transactions_from_ally(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    '''...'''

    transactions.columns = transactions.columns.str.strip()
    transactions.columns = transactions.columns.str.lower()

    transactions['account'] = 'ally'

    return transactions[[
        'account',
        'date',
        'amount',
        'description',
    ]]
