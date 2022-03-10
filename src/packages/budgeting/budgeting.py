'''...'''

import os
from typing import *

import pandas as pd

from . import transactions
from . import utils


def parse_transactions(
    data_dir: str,
    upload_dir: str,
    *,
    regex: Optional[Dict[str, str]],
    tag_update: Optional[List[Union[Dict[str, str], str]]],
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

    if regex is not None:
        utils.register_regex(**regex)  # TODO: To migrate these, you'll need to define the io_manager here and pass it to the Transactions instead of the data_path (which makes more sense anyways).
    if tag_update is not None:
        utils.register_tag_update(*tag_update)

    all_transactions = transactions.Transactions(data_dir=data_dir)
    for file in os.listdir(upload_dir):
        new_transactions = pd.read_csv(os.path.join(upload_dir, file))  # TODO: Use io_manager to do this.
        account = utils.identify_account(file, new_transactions)
        all_transactions.add_transactions(account, new_transactions)

    all_transactions.save()

    return all_transactions
