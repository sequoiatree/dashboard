'''...'''

import os
from typing import *

import pandas as pd

from . import constants
from . import enums


class Parser:
    '''...'''

    def __init__(
        self,
        upload_dir: str,
    ) -> None:
        '''...'''

        self._parsed_files = set()
        self._upload_dir = upload_dir

    def __iter__(
        self,
    ) -> Iterator[str]:
        '''...'''

        return iter(os.listdir(self._upload_dir))

    def clear(
        self,
    ) -> None:
        '''...'''

        for file in self._parsed_files:
            os.remove(self._path(file))

        self._parsed_files.clear()

    def parse_transactions(
        self,
        file: str,
    ) -> pd.DataFrame:
        '''...'''

        try:
            transactions = pd.read_csv(self._path(file), dtype='string')
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

        self._parsed_files.add(file)

        return transactions

    def _path(
        self,
        file: str,
    ) -> str:
        '''...'''

        return os.path.join(self._upload_dir, file)


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
