import shutil
from pathlib import Path

from PIL import Image
import pytesseract

from card import Card, CardType
import json
import click

CUBE_URL = "https://github.com/gabrielrussoc/boozecube/releases/download/0.0.0/cube.tar.gz"


def setup_tesseract() -> None:
    tesseract = shutil.which("tesseract")
    if tesseract is None:
        raise Exception("tesseract binary not found. Install it and add to PATH.")
    pytesseract.pytesseract.tesseract_cmd = tesseract


@click.command()
@click.argument("dir_name", type=click.Path(exists=True), default="cube")
@click.option("--urls-file", type=click.Path(exists=True, dir_okay=False), default="cube/urls.json")
def main(dir_name: str, urls_file: str) -> None:
    setup_tesseract()
    all_cards = list(Path(dir_name).glob("*.jpg"))

    with click.progressbar(length=len(all_cards), label="OCRing all cards...") as bar:

        with open(Path(urls_file)) as f:
            image_urls = json.loads(f.read())

        cards = []
        for f in all_cards:
            bar.update(1)
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
            type_str = pytesseract.image_to_string(type_img, config="--psm 7").strip()
            description = pytesseract.image_to_string(description_img, config="--psm 6").strip()
            power = pytesseract.image_to_string(power_img, config="--psm 7").strip()

            # HACK: URL is file name
            cards.append(Card(name=name, description=description, picurl=image_urls[str(f.name)],
                              type=CardType.from_text(type_str)))

    from cockatrice import create_database
    with open("database.xml", "w") as f:
        f.write(create_database(cards))


if __name__ == "__main__":
    main()

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
