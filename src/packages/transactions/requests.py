'''Requests.'''

from typing import *

from . import io
from . import parsing
from . import transactions


def request_transactions(
    data_dir: str,
    upload_dir: str,
    *,
    regex: Optional[Dict[str, str]],
    tag_update: Optional[Dict[str, Union[Dict[str, str], str]]],
) -> str:
    '''Requests the transactions described by the given files.

    Args:
        data_dir: The path to a directory of persistent local data (e.g. old
            transaction data from previous analysis).
        upload_dir: The path to a directory of new uploads (e.g. new transaction
            data downloaded from bank accounts).
        regex: A new RegEx alias for cleaning matching transactions'
            descriptions.
        tag_update: A new tag for an inaccurately tagged transaction.

    Returns:
        The transactions requested.
    '''

    io_manager = io.IOManager(data_dir)
    parser = parsing.Parser(upload_dir)

    if regex is not None:
        io.register_regex(io_manager, **regex)
    if tag_update is not None:
        io.register_tag_update(io_manager, **tag_update)

    all_transactions = transactions.Transactions(io_manager)
    for file in parser:
        new_transactions = parser.parse_transactions(file)
        all_transactions.add_transactions(new_transactions)

    all_transactions.save()
    parser.clear()

    return all_transactions
