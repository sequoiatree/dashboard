'''...'''

from typing import *

from . import enums


JSON = Dict[str, Optional[Union[int, float, str, bool, List['JSON'], 'JSON']]]  # TODO: Move to a constants.py so you don't have to define this here AND in io_manager.py.


class Configs:
    '''...'''

    def __init__(
        self,
        configs: JSON,
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
    ) -> JSON:
        '''...'''

        if key not in self._configs:
            raise KeyError()  # TODO: Write a helpful user-friendly message here (missing config). Print the absolute path to the config file too.

        return self._configs[key]
