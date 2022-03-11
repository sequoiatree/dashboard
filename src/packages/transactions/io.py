'''...'''

import datetime
import json
import os
from typing import *

import pandas as pd

from . import configs
from . import constants
from . import enums
from . import utils


class IOManager:
    '''...'''

    def __init__(
        self,
        data_dir: str,
    ) -> None:
        '''...

        Args:
            data_dir:

        Returns:
            None.
        '''

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
        '''...'''

        if cached and target in self._cache:
            return self._cache[target]

        if target is enums.Data.aliases:
            contents = self._load_json(target.value)
        elif target is enums.Data.configs:
            contents = configs.Configs(self._load_json(target.value))
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
        '''...'''

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
        '''...

        Args:
            target:
            update_function:    # can be mutative
            load_options:
            save_options:

        Returns:
            None.
        '''

        old_contents = self.load(target, **load_options)
        new_contents = update_function(old_contents)

        self._use_temp, use_temp = True, self._use_temp
        temp_path = self.save(target, new_contents, **save_options)
        path = temp_path[:-len(constants.TEMP_EXTENSION)]
        self._use_temp = use_temp

        os.rename(temp_path, path)

        if target in self._cache:
            del self._cache[target]

        return path

    def _path(
        self,
        file: str,
    ) -> str:
        '''...'''

        path = os.path.join(self._data_dir, file)

        if self._use_temp:
            path = f'{path}{constants.TEMP_EXTENSION}'

        return path

    def _load_json(
        self,
        file: str,
    ) -> constants.JSON:
        '''...'''

        try:
            with open(self._path(f'{file}.json')) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _load_table(
        self,
        file: str,
        columns: Dict[str, pd.Series],
    ) -> pd.DataFrame:
        '''...'''

        try:
            table = pd.read_csv(self._path(f'{file}.csv'), dtype='string')
            return table.assign(**{
                column_name: table[column_name].astype(columns[column_name])
                for column_name in table.columns
            })
        except FileNotFoundError:
            return pd.DataFrame({
                column_name: pd.Series(dtype=column_type)
                for column_name, column_type in columns.items()
            })

    def _save_json(
        self,
        file: str,
        data: constants.JSON,
    ) -> str:
        '''...'''

        path = self._path(f'{file}.json')
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

        return path

    def _save_table(
        self,
        file: str,
        table: pd.DataFrame,
    ) -> str:
        '''...'''

        path = self._path(f'{file}.csv')
        table.to_csv(path, index=False)

        return path


def register_regex(
    io_manager: IOManager,
    pattern: str,
    alias: Optional[str],
) -> None:
    '''...

    Args:
        pattern:
        alias:

    Returns:
        None.
    '''

    pattern = f'^{pattern}$'
    if not utils.is_valid_regex(pattern):
        return

    def update_aliases(
        aliases: Dict[str, str],
    ) -> Dict[str, str]:
        '''...'''

        aliases.update({pattern: alias and alias.upper()})
        return aliases

    io_manager.update(enums.Data.aliases, update_aliases)


def register_tag_update(
    io_manager: IOManager,
    serialized_datum: Dict[str, str],
    new_tag: str,
) -> None:
    '''...

    Args:
        serialized_datum:
        new_tag:

    Returns:
        None.
    '''

    def update_saved_tags(
        saved_tags: pd.DataFrame,
    ) -> pd.DataFrame:
        '''...'''

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
