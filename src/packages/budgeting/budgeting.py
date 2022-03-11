'''...'''

import os
from typing import *

import pandas as pd

from . import io_manager
from . import transactions
from . import utils


def parse_transactions(
    data_dir: str,
    upload_dir: str,
    *,
    regex: Optional[Dict[str, str]],
    tag_update: Optional[Dict[str, Union[Dict[str, str], str]]],
) -> str:
    '''...

    Args:
        data_dir:
        upload_dir:
        regex:
        tag_update:

    Returns:
        ...
    '''

    transactions_io_manager = io_manager.IOManager(data_dir)

    if regex is not None:
        utils.register_regex(transactions_io_manager, **regex)
    if tag_update is not None:
        utils.register_tag_update(transactions_io_manager, **tag_update)

    all_transactions = transactions.Transactions(transactions_io_manager)
    for file in os.listdir(upload_dir):
        try:
            path = os.path.join(upload_dir, file)
            new_transactions = pd.read_csv(path, dtype='string')  # TODO: abtract this try/except into a dedicated parsing file, along with parse_transactions_from_ally etc
        except Exception as exception:
            raise ValueError() from exception  # TODO - include a helpful error message
        account = utils.identify_account(file, new_transactions)
        all_transactions.add_transactions(account, new_transactions)

    all_transactions.save()

    return all_transactions
