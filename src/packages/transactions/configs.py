'''Configs.'''

from typing import *

from . import constants


class Configs:
    '''Exposes a JSON configuration object via a user-friendly API.'''

    def __init__(
        self,
        configs: constants.JSON,
    ) -> None:
        '''Initializes the Configs instance.'''

        self._configs = configs

    def __getitem__(
        self,
        key: str,
    ) -> constants.JSON:
        '''Gets the requested config.'''

        if key not in self._configs:
            raise KeyError()  # TODO: Write a helpful user-friendly message here (missing config). Print the absolute path to the config file too.

        return self._configs[key]
