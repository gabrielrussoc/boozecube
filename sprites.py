from PIL import Image
from util import pilToCv

icons = Image.open("icons/all.png")

# There 10 icons per row, icons are square
SZ = icons.width / 10

# Size of the icons on the actual cards
CARD_SZ = 20


# 0-indexed
# (0,0) (0,1) (0,2)
# (1,0) (1,1)
# (2,0)
def crop(i, j):
    return pilToCv(icons.crop((j * SZ, i * SZ, (j + 1) * SZ, (i + 1) * SZ)).resize((CARD_SZ, CARD_SZ)))


ZERO = crop(0, 0)
ONE = crop(0, 1)
TWO = crop(0, 2)
WHITE = crop(2, 4)
BLUE = crop(2, 5)
BLACK = crop(2, 6)
RED = crop(2, 7)
GREEN = crop(2, 8)
