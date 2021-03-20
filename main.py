import shutil
import glob

from PIL import Image
import pytesseract

from card import Card, CardType
import progressbar
import json

CUBE_URL = "https://github.com/gabrielrussoc/boozecube/releases/download/0.0.0/cube.tar.gz"

pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")

all_cards = glob.glob("cube/*.jpg")

bar = progressbar.ProgressBar(maxval=len(all_cards), \
                              widgets=[progressbar.SimpleProgress()])
bar.start()

print("OCRing all cards...")

with open("cube/urls.json") as f:
    image_urls = json.loads(f.read())

cards = []
for i, f in enumerate(all_cards):
    bar.update(i+1)
    card_img = Image.open(f)

    NAME_BOX = (30, 30, 300, 52)
    MANA_BOX = (250, 30, 345, 52)
    TYPE_BOX = (32, 300, 320, 318)
    DESCRIPTION_BOX = (30, 330, 340, 465)
    POWER_BOX = (290, 470, 340, 490)

    name_img = card_img.crop(NAME_BOX)
    mana_img = card_img.crop(MANA_BOX)
    type_img = card_img.crop(TYPE_BOX)
    description_img = card_img.crop(DESCRIPTION_BOX)
    power_img = card_img.crop(POWER_BOX)

    # Page segmentation modes:
    #   0    Orientation and script detection (OSD) only.
    #   1    Automatic page segmentation with OSD.
    #   2    Automatic page segmentation, but no OSD, or OCR.
    #   3    Fully automatic page segmentation, but no OSD. (Default)
    #   4    Assume a single column of text of variable sizes.
    #   5    Assume a single uniform block of vertically aligned text.
    #   6    Assume a single uniform block of text.
    #   7    Treat the image as a single text line.
    #   8    Treat the image as a single word.
    #   9    Treat the image as a single word in a circle.
    #  10    Treat the image as a single character.
    #  11    Sparse text. Find as much text as possible in no particular order.
    #  12    Sparse text with OSD.
    #  13    Raw line. Treat the image as a single text line,
    name = pytesseract.image_to_string(name_img, config="--psm 7").strip()
    type = pytesseract.image_to_string(type_img, config="--psm 7").strip()
    description = pytesseract.image_to_string(description_img, config="--psm 6").strip()
    power = pytesseract.image_to_string(power_img, config="--psm 7").strip()

    # HACK: URL is file name
    cards.append(Card(name=name, description=description, picurl=image_urls[f.strip("cube/")], type=CardType.from_text(type)))

bar.finish()

from cockatrice import create_database
with open("database.xml", "w") as f:
    f.write(create_database(cards))



# Playing around with mana
# import cv2
# import numpy
# from sprites import ZERO, ONE, TWO, WHITE
# from util import pilToCv
#
# mana_img_opencv = pilToCv(card_img)
#
# results = cv2.matchTemplate(mana_img_opencv, WHITE, cv2.TM_CCOEFF_NORMED)
# locations = numpy.where( results >= 0.6)
# print(locations)
# for pt in zip(*locations[::-1]):
#     cv2.rectangle(mana_img_opencv, pt, (pt[0] + 20, pt[1] + 20), (0, 0, 0), 2)
#
# cv2.imwrite("a.png", mana_img_opencv)
# mana_img.show()

