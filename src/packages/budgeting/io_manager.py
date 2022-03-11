'''...'''

import json
import os
from typing import *

import pandas as pd

from . import configs
from . import enums


JSON = Dict[str, Optional[Union[int, float, str, bool, List['JSON'], 'JSON']]]
TEMP_EXTENSION = '.tmp'


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

        self._data_dir = data_dir
        self._use_temp = False

    def load(
        self,
        target: enums.Data,
        **options: Any,
    ) -> Any:
        '''...'''

        if target is enums.Data.aliases:
            return self._load_json(target.value)
        if target is enums.Data.configs:
            return configs.Configs(self._load_json(target.value))
        if target is enums.Data.saved_tags:
            return self._load_table(target.value, **options)
        if target is enums.Data.transactions:
            return self._load_table(target.value, **options)
        raise ValueError()  # TODO

    def save(
        self,
        target: enums.Data,
        to_save: Any,
        **options: Any,
    ) -> str:
        '''...'''

        if target is enums.Data.aliases:
            return self._save_json(target.value, to_save, **options)
        if target is enums.Data.saved_tags:
            return self._save_table(target.value, to_save, **options)
        if target is enums.Data.transactions:
            return self._save_table(target.value, to_save, **options)
        raise ValueError()  # TODO

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
        path = temp_path[:-len(TEMP_EXTENSION)]
        self._use_temp = use_temp

        os.rename(temp_path, path)

        return path

    def _path(
        self,
        file: str,
    ) -> str:
        '''...'''

        path = os.path.join(self._data_dir, file)

        if self._use_temp:
            path = f'{path}{TEMP_EXTENSION}'

        return path

    def _load_json(
        self,
        file: str,
    ) -> JSON:
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
            return pd.read_pickle(self._path(f'{file}.pickle'))  # TODO: Save as CSV instead of .pickle so you can read them. Just make sure column dtypes are preserved (or set when loaded from file).
        except FileNotFoundError:
            return pd.DataFrame(columns)

    def _save_json(
        self,
        file: str,
        data: JSON,
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

        path = self._path(f'{file}.pickle')
        table.to_pickle(path)

        return path
