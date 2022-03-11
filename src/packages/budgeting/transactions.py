'''...'''

import calendar
import datetime
from typing import *

import numpy as np
import pandas as pd

from . import constants
from . import enums
from . import io_manager
from . import utils


class Transactions:
    '''...'''

    def __init__(
        self,
        io_manager: io_manager.IOManager,
    ) -> None:
        '''...

        Args:
            io_manager:

        Returns:
            None.
        '''

        self._io_manager = io_manager
        self._aliases = self._io_manager.load(enums.Data.aliases)  # TODO: Load lazily instead of loading all at the beginning. Maybe make a convenience _get function that calls io_manager.load()?
        self._configs = self._io_manager.load(enums.Data.configs)
        self._transactions = self._io_manager.load(
            enums.Data.transactions,
            columns=constants.TRANSACTIONS_COLUMNS,
        )
        self._saved_tags = self._io_manager.load(
            enums.Data.saved_tags,
            columns=constants.SAVED_TAGS_COLUMNS,
        )

        self._postprocessed_transactions = None

    def add_transactions(
        self,
        account: enums.Account,
        transactions: pd.DataFrame,
    ) -> None:
        '''...

        Args:
            account:
            transactions:

        Returns:
            None.

        Raises:
            ...
        '''

        if account is enums.Account.ally:
            transactions = parse_transactions_from_ally(transactions)
        # elif account is enums.Account.____:
        #     transactions = parse_transactions_from_____(transactions)
        else:
            raise ValueError(...)  # TODO

        new_transactions = (
            self._transactions
            .merge(transactions, how='outer', indicator=True)
            .loc[lambda union: union['_merge'] == 'right_only']
            .drop('_merge', axis=1)
        )

        self._transactions = (
            self._transactions
            .append(new_transactions)
            .reset_index(drop=True)
        )
        self._postprocessed_transactions = None

    def transactions(
        self,
    ) -> pd.DataFrame:
        '''...'''

        if self._postprocessed_transactions is None:
            self._postprocessed_transactions = (
                self._transactions
                .pipe(with_clean_descriptions, aliases=self._aliases)
                .pipe(with_tags, saved_tags=self._saved_tags)
                .sort_values('date', ascending=False)
            )

        return self._postprocessed_transactions

    def metrics(
        self,
    ) -> pd.DataFrame:
        '''...'''

        transactions = self.transactions().pipe(select_recent, since=1)

        monthly_budget = self._configs['budget']
        current_month = utils.months_ago(0)

        total = lambda transactions: transactions['amount'].sum()
        is_tagged = lambda transactions, tag: transactions[transactions['tag'] == tag.value]
        datum = lambda amount, description: {
            'amount': amount,
            'description': description,
        }

        def ytd_metrics(
        ) -> pd.DataFrame:
            '''...

            Returns:
                ...
            '''

            ytd_budget = monthly_budget * current_month

            totals = {
                tag: total(
                    transactions
                    .pipe(is_tagged, tag=tag)
                )
                for tag in enums.Tag
            }
            spending = totals[enums.Tag.spending]

            return pd.DataFrame([
                *[
                    datum(total / current_month, f'AVG. {tag.value.upper()}')
                    for tag, total in totals.items()
                    if tag is not enums.Tag.spending
                ],
                datum(*utils.budget_status(ytd_budget, spending)),
            ])

        def month_metrics(
            month: int,
        ) -> pd.DataFrame:
            '''...

            Args:
                month:

            Returns:
                ...
            '''

            for_month = lambda transactions: transactions.pipe(
                select_recent,
                since=month,
                to_present=False,
            )

            totals = {
                tag: total(
                    transactions
                    .pipe(for_month)
                    .pipe(is_tagged, tag=tag)
                )
                for tag in enums.Tag
            }
            spending = totals[enums.Tag.spending]

            return pd.DataFrame([
                *[
                    datum(total, tag.value.upper())
                    for tag, total in totals.items()
                ],
                datum(*utils.budget_status(monthly_budget, spending)),
            ])

        metrics = [
            {
                'period': calendar.month_name[month],
                'metrics': month_metrics(month),
            }
            for month in [utils.months_ago(1), utils.months_ago(0)]
        ]
        metrics[-1]['period'] = '\n'.join((metrics[-1]['period'], '(so far)'))
        metrics.append({
            'period': 'Year-to-Date',
            'metrics': ytd_metrics(),
        })

        return metrics

    def save(
        self,
    ) -> None:
        '''...'''

        self._io_manager.save(enums.Data.saved_tags, self._saved_tags)
        self._io_manager.save(enums.Data.transactions, self._transactions)

    def to_dict(
        self,
    ) -> str:
        '''...'''

        def serialize(
            object: Any,
        ) -> Any:
            '''...

            Args:
                object:

            Returns:
                ...
            '''

            if isinstance(object, pd.DataFrame):
                return (
                    object
                    .pipe(utils.stringify_columns)
                    .to_dict(orient='records')
                )
            if isinstance(object, dict):
                return {
                    key: serialize(value)
                    for key, value in object.items()
                }
            if isinstance(object, list):
                return [
                    serialize(value)
                    for value in object
                ]
            if isinstance(object, str):
                return object
            raise TypeError(...)  # TODO

        return {
            'transactions': serialize(
                self.transactions()
                .pipe(select_recent, since=utils.months_ago(1))
            ),
            'metrics': serialize(self.metrics()),
            'tags': [tag.value for tag in enums.Tag],
        }


def parse_transactions_from_ally(  # TODO: Move to utils or enums. Or dedicated parsing file?
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    '''...'''  # return [str account, pd.Timestamp date, float amount, str description]

    transactions.columns = transactions.columns.str.strip()
    transactions.columns = transactions.columns.str.lower()

    transactions['account'] = 'ally'

    transactions = transactions[[
        'account',
        'date',
        'amount',
        'description',
    ]]

    return transactions.assign(date=pd.to_datetime(transactions['date']))


def with_clean_descriptions(  # TODO: Move to utils.
    transactions: pd.DataFrame,
    aliases: Dict[str, Optional[str]],
) -> pd.DataFrame:
    '''...

    Args:
        transactions:
        aliases:

    Returns:
        ...
    '''

    patterns_to_sub = {}
    patterns_to_del = []
    for pattern, alias in aliases.items():
        if alias is None:
            patterns_to_del.append(pattern)
        else:
            patterns_to_sub[pattern] = alias

    clean = lambda column: (
        column
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
        .str.upper()
    )

    clean_descriptions = (
        transactions['description']
        .pipe(clean)
        .str.replace(r'(?<=\w) (?=\.COM)', '', regex=True)  # Websites.
        .str.replace(r'(?<!\w)\d{3}[- ]?\d{3}[- ]?\d{4}(?!\w)', '', regex=True)  # Phone numbers.
        .str.replace(r'~ FUTURE AMOUNT: \d+(\.\d\d)? ~ TRAN: DDIR$', '', regex=True)  # Direct deposit.
        .str.replace(r'(, \w\w)+$', '', regex=True)  # City, state, country.
        .pipe(clean)
    )

    for pattern, alias in patterns_to_sub.items():
        clean_descriptions = (
            clean_descriptions
            .str.replace(pattern, alias, regex=True)
        )
    transactions = transactions.assign(clean_description=clean_descriptions)

    data_to_del = np.logical_or.reduce(
        [
            clean_descriptions.str.contains(pattern, regex=True)
            for pattern in patterns_to_del
        ],
        dtype=bool,
    )
    if isinstance(data_to_del, np.ndarray):
        transactions = transactions[~data_to_del].reset_index(drop=True)

    return transactions


def with_tags(  # TODO: Move to utils.
    transactions: pd.DataFrame,
    saved_tags: pd.DataFrame,
) -> pd.DataFrame:
    '''
        ...

    Args:
        transactions:

    Returns:
        ...
    '''

    tags = pd.Series('', index=transactions.index, dtype='string')

    is_expense = transactions['amount'] < 0
    is_property_transaction = transactions['clean_description'].isin([
        'RYLAND MEWS MORTGAGE',
        'RYLAND MEWS HOA',
        'PG&E',
    ])
    is_other_transaction = ~is_property_transaction

    tags[is_expense & is_property_transaction] = enums.Tag.property_expense.value
    tags[is_expense & is_other_transaction] = enums.Tag.spending.value

    return (
        transactions
        .assign(tag=tags)
        .merge(saved_tags.rename(columns={'tag': 'saved_tag'}), how='left')
        .assign(tag=lambda merged: merged['saved_tag'].fillna(merged['tag']))
        .drop('saved_tag', axis=1)
    )


def select_recent(  # TODO: Move to utils.
    transactions: pd.DataFrame,
    *,
    since: int,
    to_present: bool = True,
) -> pd.DataFrame:
    '''...

    Args:
        transactions:
        since:            month identifier, 1-indexed for consistency w datetime
        to_present:       T = from that month to now, F = just that month

    Returns:
        ...
    '''

    current_month = utils.months_ago(0)
    cutoff = datetime.date(
        datetime.date.today().year - (current_month < since),
        since,
        1,
    )

    dates = transactions['date'].map(lambda date: date.date())
    months = transactions['date'].map(lambda date: date.month)

    data_to_keep = (dates >= cutoff) & (to_present or months == cutoff.month)

    return transactions[data_to_keep]
