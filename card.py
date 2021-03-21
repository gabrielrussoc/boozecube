from dataclasses import dataclass
from enum import Enum
from fuzzywuzzy import fuzz


def _best_match(pat: str, text: str) -> int:
    ratio = fuzz.partial_ratio(pat.lower(), text.lower())
    if ratio > 90:
        return 100
    elif ratio < 50:
        return 0
    else:
        return ratio


# TODO: What if a card has two types? e.g. Artifact creature
class CardType(Enum):
    # Token cards don't have the card type on the same location, so we will process some trash text and default to
    # token because it has priority.
    TOKEN = "Token"
    LAND = "Land"
    # Creature must be before Artifact or Enchantment because it has priority
    CREATURE = "Creature"
    SORCERY = "Sorcery"
    INSTANT = "Instant"
    ENCHANTMENT = "Enchantment"
    ARTIFACT = "Artifact"

    @staticmethod
    def from_text(text: str) -> "CardType":
        all_types = list(CardType)
        types_with_matches = [
            (tp, _best_match(tp.value, text)) for tp in all_types
        ]
        return max(types_with_matches, key=lambda v: v[1])[0]


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
    type: CardType
    enters_tapped = False
    rarity: CardRarity = CardRarity.COMMON
    layout: CardLayout = CardLayout.NORMAL
    mana = None  # TODO
