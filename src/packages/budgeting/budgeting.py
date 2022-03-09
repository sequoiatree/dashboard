'''...'''

import os
from typing import *

import pandas as pd

from . import transactions
from . import utils


def parse_transactions(
    transactions_dir: str,
    *,
    regex: Optional[Dict[str, str]],
    tag_update: Optional[List[Union[Dict[str, str], str]]],
) -> str:
    '''...

    Args:
        transactions_dir:
        regex:

    Returns:
        ...
    '''

    if regex is not None:
        utils.register_regex(**regex)
    if tag_update is not None:
        utils.register_tag_update(*tag_update)

    all_transactions = transactions.Transactions()
    for file in os.listdir(transactions_dir):
        new_transactions = pd.read_csv(os.path.join(transactions_dir, file))
        account = utils.identify_account(file, new_transactions)
        all_transactions.add_transactions(account, new_transactions)

    all_transactions.save()

    return all_transactions
