'''...'''

import json
import os
from typing import *

import pandas as pd

from . import configs
from . import enums


JSON = Dict[str, Optional[Union[int, float, str, bool, List['JSON'], 'JSON']]]


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
        **options: Any,
    ) -> None:
        '''...'''

        if target is enums.Data.saved_tags:
            return self._save_table(target.value, **options)
        if target is enums.Data.transactions:
            return self._save_table(target.value, **options)
        raise ValueError()  # TODO

    def _path(
        self,
        file: str,
    ) -> str:
        '''...'''

        return os.path.join(self._data_dir, file)

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
            return pd.read_pickle(self._path(f'{file}.pickle'))
        except FileNotFoundError:
            return pd.DataFrame(columns)

    def _save_table(
        self,
        file: str,
        table: pd.DataFrame,
    ) -> None:
        '''...'''

        return table.to_pickle(self._path(f'{file}.pickle'))
