'''I/O utilities.'''

import datetime
import json
import os
from typing import *

import pandas as pd

from . import configs
from . import constants
from . import enums
from . import utils


TEMP_EXTENSION = '.tmp'


class IOManager:
    '''Handles I/O operations for a set of pre-defined data files.'''

    def __init__(
        self,
        data_dir: str,
    ) -> None:
        '''Initializes the IOManager.'''

        self._cache = {}
        self._data_dir = data_dir
        self._use_temp = False

    def load(
        self,
        target: enums.Data,
        cached: bool=True,
        /,
        **options: Any,
    ) -> Any:
        '''Loads the requested target.'''

        if cached and target in self._cache:
            return self._cache[target]

        if target is enums.Data.aliases:
            contents = self._load_json(target.value, **options)
        elif target is enums.Data.configs:
            contents = configs.Configs(
                self._path(f'{target.value}.json'),
                self._load_json(target.value, **options),
            )
        elif target is enums.Data.saved_tags:
            contents = self._load_table(target.value, **options)
        elif target is enums.Data.transactions:
            contents = self._load_table(target.value, **options)
        else:
            raise ValueError(utils.error_message(
                f'The load target {target} is invalid or unsupported.',
                target=target,
            ))

        self._cache[target] = contents

        return contents

    def save(
        self,
        target: enums.Data,
        to_save: Any,
        /,
        **options: Any,
    ) -> str:
        '''Saves the requested target.'''

        if target is enums.Data.aliases:
            path = self._save_json(target.value, to_save, **options)
        elif target is enums.Data.saved_tags:
            path = self._save_table(target.value, to_save, **options)
        elif target is enums.Data.transactions:
            path = self._save_table(target.value, to_save, **options)
        else:
            raise ValueError(utils.error_message(
                f'The save target {target} is invalid or unsupported.',
                target=target,
            ))

        return path

    def update(
        self,
        target: enums.Data,
        update_function: Callable[[Any], Any],
        *,
        load_options: Dict[str, Any] = {},
        save_options: Dict[str, Any] = {},
    ) -> str:
        '''Updates the requested target per the given update function.

        The update function's singular parameter should be the object received
        by loading the target with the given load options. The function may or
        may not be mutative, but either way it should return an updated object
        to be saved with the given save optioins.
        '''

        old_contents = self.load(target, **load_options)
        new_contents = update_function(old_contents)

        self._use_temp, use_temp = True, self._use_temp
        temp_path = self.save(target, new_contents, **save_options)
        path = temp_path[:-len(TEMP_EXTENSION)]
        self._use_temp = use_temp

        os.rename(temp_path, path)

        if target in self._cache:
            del self._cache[target]

        return path

    def _path(
        self,
        file: str,
    ) -> str:
        '''Gets the path to the requested file in the data directory.'''

        path = os.path.join(self._data_dir, file)

        if self._use_temp:
            path = f'{path}{TEMP_EXTENSION}'

        return path

    def _load_json(
        self,
        file: str,
    ) -> constants.JSON:
        '''Loads a JSON-like Python object from a JSON file.'''

        path = self._path(f'{file}.json')
        try:
            with open(path) as f:
                json_object = json.load(f)
        except FileNotFoundError:
            json_object = {}

        return json_object

    def _load_table(
        self,
        file: str,
        columns: Dict[str, pd.Series],
    ) -> pd.DataFrame:
        '''Loads a Pandas DataFrame from a CSV file.'''

        path = self._path(f'{file}.csv')
        try:
            table = pd.read_csv(path, dtype='string')
        except FileNotFoundError:
            table = pd.DataFrame(columns=list(columns))

        # TODO: Check columns match set(columns).

        return table.astype(columns)

    def _save_json(
        self,
        file: str,
        data: constants.JSON,
    ) -> str:
        '''Saves a JSON-like Python object to a JSON file.'''

        path = self._path(f'{file}.json')
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

        return path

    def _save_table(
        self,
        file: str,
        table: pd.DataFrame,
    ) -> str:
        '''Saves a Pandas DataFrame to a CSV file.'''

        path = self._path(f'{file}.csv')
        table.to_csv(path, index=False)

        return path


def register_regex(
    io_manager: IOManager,
    pattern: str,
    alias: Optional[str],
) -> None:
    '''Updates the `aliases` target with a new substitution or deletion rule.

    `Transactions` instances use the rules defined by this target to clean up
    the descriptions associated with financial transactions.

    Args:
        io_manager: The `IOManager` that should handle the update.
        pattern: A RegEx pattern matching the descriptions that should be
            replaced or deleted.
        alias: The new text that should replace the descriptions matching the
            given pattern, or `None` to instead delete the transactions
            associated with those descriptions.

    Returns:
        None.
    '''

    pattern = f'^{pattern}$'
    if not utils.is_valid_regex(pattern):
        return

    def update_aliases(
        aliases: Dict[str, str],
    ) -> Dict[str, str]:

        aliases.update({pattern: alias and alias.upper()})
        return aliases

    io_manager.update(enums.Data.aliases, update_aliases)


def register_tag_update(
    io_manager: IOManager,
    serialized_datum: Dict[str, str],
    new_tag: str,
) -> None:
    '''Updates the `saved_tags` target with a new tag for a transaction.

    `Transactions` instances use the tags defined by this target to correct
    inaccuracies in the tags automatically assigned to financial transactions.

    Args:
        serialized_datum: A JSON-like representation of the transaction whose
            tag should be changed.
        new_tag: The new tag that should be associated with the transaction.

    Returns:
        None.
    '''

    def update_saved_tags(
        saved_tags: pd.DataFrame,
    ) -> pd.DataFrame:

        year = datetime.date.today().year
        date = datetime.datetime.strptime(serialized_datum['date'], '%a, %b. %d')
        datum = pd.DataFrame(
            {
                'account': serialized_datum['account'],
                'date': pd.Timestamp(datetime.date(year, date.month, date.day)),
                'amount': float(serialized_datum['amount']),
                'description': serialized_datum['description'],
                'tag': new_tag,
            },
            index=[0],
        )

        saved_tags_to_keep = (
            saved_tags
            .merge(datum.drop('tag', axis=1), how='outer', indicator=True)
            .loc[lambda union: union['_merge'] == 'left_only']
            .drop('_merge', axis=1)
        )

        return (
            saved_tags_to_keep
            .append(datum)
            .reset_index(drop=True)
        )

    io_manager.update(
        enums.Data.saved_tags,
        update_saved_tags,
        load_options=dict(
            columns=constants.SAVED_TAGS_COLUMNS,
        ),
    )
