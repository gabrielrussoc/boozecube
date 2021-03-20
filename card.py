from dataclasses import dataclass
from enum import Enum
from fuzzysearch import find_near_matches


def _best_match(pat: str, text: str) -> int:
    return min([match.dist for match in find_near_matches(pat.lower(), text.lower(), max_l_dist=4)] + [100])


# TODO: What if a card has two types? e.g. Artifact creature
class CardType(Enum):
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
        return min(types_with_matches, key=lambda v: v[1])[0]



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
    token: bool = False
    enters_tapped = False
    rarity: CardRarity = CardRarity.COMMON
    layout: CardLayout = CardLayout.NORMAL
    mana = None  # TODO
