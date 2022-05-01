'''Transactions.'''

import calendar
import datetime
from typing import *

import numpy as np
import pandas as pd

from . import constants
from . import encoders
from . import enums
from . import io
from . import utils


class Transactions:
    '''Models financial transactions and exposes an API for simple analysis.'''

    def __init__(
        self,
        io_manager: io.IOManager,
    ) -> None:
        '''Initializes the `Transactions` instance.'''

        self._io_manager = io_manager
        self._transactions = self._get(enums.Data.transactions)
        self._postprocessed_transactions = None

    def _get(
        self,
        target: enums.Data,
    ) -> Any:
        '''Loads the requested target.'''

        if target is enums.Data.aliases:
            return self._io_manager.load(enums.Data.aliases)
        elif target is enums.Data.configs:
            return self._io_manager.load(enums.Data.configs)
        elif target is enums.Data.saved_tags:
            return self._io_manager.load(
                enums.Data.saved_tags,
                columns=constants.SAVED_TAGS_COLUMNS,
            )
        elif target is enums.Data.transactions:
            return self._io_manager.load(
                enums.Data.transactions,
                columns=constants.TRANSACTIONS_COLUMNS,
            )
        else:
            raise ValueError(utils.error_message(
                'The load target {target} is invalid or unsupported.',
                target=target,
            ))

    def add_transactions(
        self,
        transactions: pd.DataFrame,
    ) -> None:
        '''Adds new transactions for the `Transactions` instance to track.'''

        new_transactions = (
            self._transactions
            .merge(transactions, how='outer', indicator=True)
            .loc[lambda merged: merged['_merge'] == 'right_only']
            .drop('_merge', axis=1)
        )

        self._transactions = (
            self._transactions
            .append(new_transactions)
            .reset_index(drop=True)
            .sort_values('date')
        )
        self._postprocessed_transactions = None

    def transactions(
        self,
    ) -> pd.DataFrame:
        '''Gets post-processed transactions, with all the desired metadata.'''

        if self._postprocessed_transactions is None:
            self._postprocessed_transactions = (
                self._transactions
                .pipe(with_clean_descriptions, aliases=self._get(enums.Data.aliases))
                .pipe(with_tags, saved_tags=self._get(enums.Data.saved_tags))
                .sort_values('date', ascending=False)
            )

        return self._postprocessed_transactions

    def metrics(
        self,
    ) -> pd.DataFrame:
        '''Gets summarizing metrics per month and for the year-to-date.'''

        transactions = self.transactions().pipe(select_recent, since=1)

        monthly_budget = self._get(enums.Data.configs)['monthly_spending_budget']
        current_month = utils.months_ago(0)

        total = lambda transactions: transactions['amount'].sum()
        is_tagged = lambda transactions, tag: transactions[transactions['tag'] == tag.value]
        totals_by_tag = lambda transactions: {
            tag: (
                transactions
                .pipe(is_tagged, tag=tag)
                .pipe(total)
            )
            for tag in enums.Tag
        }
        datum = lambda amount, description: {
            'amount': amount,
            'description': description,
        }

        def budget_status(
            budget: float,
            spending: float,
        ) -> Tuple[float, str]:

            buffer = budget - abs(spending)
            status = 'OVER BUDGET' if buffer < 0 else 'WITHIN BUDGET'

            return buffer, status

        def month_metrics(
            month: int,
        ) -> pd.DataFrame:

            transactions_for_month = (
                transactions
                .pipe(select_recent, since=month, to_present=False)
            )

            totals = totals_by_tag(transactions_for_month)

            return pd.DataFrame([
                *[
                    datum(totals[tag], tag.value.upper())
                    for tag in (
                        enums.Tag.property_expense,
                        enums.Tag.spending,
                    )
                ],
                datum(*budget_status(
                    monthly_budget,
                    totals[enums.Tag.spending],
                )),
            ])

        def ytd_metrics(
        ) -> pd.DataFrame:

            average = lambda total: total / current_month

            totals = totals_by_tag(transactions)

            return pd.DataFrame([
                *[
                    datum(average(totals[tag]), f'AVG. {tag.value.upper()}')
                    for tag in (
                        enums.Tag.property_expense,
                    )
                ],
                *[
                    datum(totals[tag], tag.value.upper())
                    for tag in (
                        enums.Tag.car_expense,
                    )
                ],
                datum(*budget_status(
                    monthly_budget * current_month,
                    totals[enums.Tag.spending],
                )),
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
        '''Saves all tracked transactions.'''

        self._io_manager.save(enums.Data.transactions, self._transactions)

    def to_json(
        self,
    ) -> str:
        '''Encodes the `Transactions` instance as a JSON string.'''

        return encoders.DataFrameJSONEncoder().encode({
            'transactions': (
                self.transactions()
                .pipe(select_recent, since=utils.months_ago(1))
            ),
            'metrics': self.metrics(),
            'tags': [tag.value for tag in enums.Tag],
        })


def with_clean_descriptions(
    transactions: pd.DataFrame,
    aliases: Dict[str, Optional[str]],
) -> pd.DataFrame:
    '''Cleans the descriptions of the given transactions.

    In addition to basic string cleaning, this involves the replacements and
    deletions specified by `aliases`.
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
        .str.replace(r'(, \w{2,3})+$', '', regex=True)  # City, state, country.
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


def with_tags(
    transactions: pd.DataFrame,
    saved_tags: pd.DataFrame,
) -> pd.DataFrame:
    '''Tags the given transactions.

    Tags loaded from `saved_tags` take priority over those automatically
    assigned to transactions, as the latter are only educated guesses.
    '''

    tags = pd.Series('', index=transactions.index, dtype='string')

    is_expense = transactions['amount'] < 0
    is_property_transaction = transactions['clean_description'].isin([
        'RYLAND MEWS MORTGAGE',
        'RYLAND MEWS HOA',
        'RYLAND MEWS PROPERTY TAX',
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


def select_recent(
    transactions: pd.DataFrame,
    *,
    since: int,
    to_present: bool = True,
) -> pd.DataFrame:
    '''Select all transactions since the specified month, or only those in it.

    Args:
        transactions: The transactions to select from.
        since: The month number, 1-indexed for consistency with the `datetime`
            module. The specified month is the most recent one corresponding to
            the month number provided. For example `since=5` specifies May 2021
            if called in January 2022, but it specifies May 2022 if called in
            June 2022.
        to_present: Whether to include all transactions since the beginning of
            the specified month, or only those in it.

    Returns:
        All transactions since the specified month, or only those in it,
        depending on the value of `to_present`.
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
