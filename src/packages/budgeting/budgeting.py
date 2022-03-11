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
    tag_update: Optional[List[Union[Dict[str, str], str]]],  # TODO: JS file should pass this as a dict, not a list!
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
        utils.register_tag_update(transactions_io_manager, *tag_update)

    all_transactions = transactions.Transactions(transactions_io_manager)
    for file in os.listdir(upload_dir):
        new_transactions = pd.read_csv(os.path.join(upload_dir, file))  # TODO: Use io_manager to do this.
        account = utils.identify_account(file, new_transactions)
        all_transactions.add_transactions(account, new_transactions)

    all_transactions.save()

    return all_transactions
