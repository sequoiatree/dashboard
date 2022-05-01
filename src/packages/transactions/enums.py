'''Enums.'''

import enum


class Account(enum.Enum):
    '''Account types.'''

    ally = 'ally'
    chase = 'chase'


class Data(enum.Enum):
    '''Local data.'''

    aliases = 'aliases'
    configs = 'configs'
    saved_tags = 'saved_tags'
    transactions = 'transactions'


class Tag(enum.Enum):
    '''Transaction tags.'''

    car_expense = 'car repairs & mods'
    property_expense = 'property expenses'
    spending = 'spending'
