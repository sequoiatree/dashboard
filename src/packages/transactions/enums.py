'''Enums.'''

import enum


class Account(enum.Enum):
    '''Account types.'''

    ally = 'ally'


class Data(enum.Enum):
    '''Local data.'''

    aliases = 'aliases'
    configs = 'configs'
    saved_tags = 'saved_tags'
    transactions = 'transactions'


class Tag(enum.Enum):
    '''Transaction tags.'''

    property_expense = 'property expenses'
    spending = 'spending'
