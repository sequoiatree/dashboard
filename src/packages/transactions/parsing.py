'''Parsing.'''

import os
from typing import *

import pandas as pd

from . import constants
from . import enums
from . import id
from . import utils


class Parser:
    '''Parses new transaction data, e.g. downloaded from bank accounts.'''

    def __init__(
        self,
        upload_dir: str,
    ) -> None:
        '''Initializes the Parser.'''

        self._parsed_files = set()
        self._upload_dir = upload_dir

    def __iter__(
        self,
    ) -> Iterator[str]:
        '''Returns an iterator over the files in the upload directory.'''

        return iter(os.listdir(self._upload_dir))

    def clear(
        self,
    ) -> None:
        '''Empties the upload directory of files that have been parsed.'''

        for file in self._parsed_files:
            os.remove(self._path(file))

        self._parsed_files.clear()

    def parse_transactions(
        self,
        file: str,
    ) -> pd.DataFrame:
        '''Parses new transaction data into a standard format.'''

        try:
            transactions = pd.read_csv(self._path(file), dtype='string')
        except Exception as exception:
            raise ValueError(utils.error_message(
                'Could not parse transactions file {path}.',
                path=self._path(file),
            )) from exception

        account = id.identify_account(file, transactions)

        if account is enums.Account.ally:
            transactions = standardize_transactions_from_ally(transactions)
        # elif account is enums.Account.____:
        #     transactions = standardize_transactions_from_____(transactions)
        else:
            raise ValueError(utils.error_message(
                'Could not standardize transaction data from {account}.',
                'You can implement the standardization logic in {code}.',
                account=account,
                code=__file__,
            ))

        transactions = transactions.astype(constants.TRANSACTIONS_COLUMNS)

        self._parsed_files.add(file)

        return transactions

    def _path(
        self,
        file: str,
    ) -> str:
        '''Gets the path to the requested file in the upload directory.'''

        return os.path.join(self._upload_dir, file)


def standardize_transactions_from_ally(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    '''Standardizes transaction data downloaded from Ally.'''

    transactions.columns = transactions.columns.str.strip()
    transactions.columns = transactions.columns.str.lower()

    transactions['account'] = 'ally'

    return transactions[list(constants.TRANSACTIONS_COLUMNS)]
