'''Configs.'''

from typing import *

from . import constants
from . import utils


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
            raise KeyError(utils.error_message(
                'The config {key} is undefined.',
                'Please define it in your configuration file.',
                key=key,
            ))

        return self._configs[key]
