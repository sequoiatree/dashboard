'''...'''

from typing import *

from . import constants


class Configs:
    '''...'''

    def __init__(
        self,
        configs: constants.JSON,
    ) -> None:
        '''...

        Args:
            configs:

        Returns:
            None.
        '''

        self._configs = configs

    def __getitem__(
        self,
        key: str,
    ) -> constants.JSON:
        '''...'''

        if key not in self._configs:
            raise KeyError()  # TODO: Write a helpful user-friendly message here (missing config). Print the absolute path to the config file too.

        return self._configs[key]
