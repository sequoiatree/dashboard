'''...'''

from typing import *

from . import io
from . import parsing
from . import transactions
from . import utils


def parse_transactions(  # TODO: Rename!
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

    io_manager = io.IOManager(data_dir)
    parser = parsing.Parser(upload_dir)

    if regex is not None:
        utils.register_regex(io_manager, **regex)
    if tag_update is not None:
        utils.register_tag_update(io_manager, **tag_update)

    all_transactions = transactions.Transactions(io_manager)
    for file in parser:
        new_transactions = parser.parse_transactions(file)
        all_transactions.add_transactions(new_transactions)

    all_transactions.save()
    parser.clear()

    return all_transactions
