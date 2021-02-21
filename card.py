from dataclasses import dataclass
from enum import Enum


# TODO: What if a card has two types? e.g. Artifact creature
class CardType(Enum):
    LAND = 0
    CREATURE = 1
    SORCERY = 2
    INSTANT = 3
    ENCHANTMENT = 4
    ARTIFACT = 5


class CardRarity(Enum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    MYTHIC = 3


class CardLayout(Enum):
    NORMAL = 0
    SPLIT = 1


@dataclass
class Card:
    name: str
    description: str
    picurl: str
    token: bool = False
    enters_tapped = False
    type: CardType = CardType.CREATURE
    rarity: CardRarity = CardRarity.COMMON
    layout: CardLayout = CardLayout.NORMAL
    mana = None #TODO
