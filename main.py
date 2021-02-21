from PIL import Image
import pytesseract

CUBE_URL = "https://github.com/gabrielrussoc/boozecube/releases/download/0.0.0/cube.tar.gz"

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# card_img = Image.open('C:/Users/gabrielrc/Documents/boozecube/Archon of Light Beer.jpg')
card_img = Image.open('C:/Users/gabrielrc/Documents/boozecube/Alkie Griffin.jpg')

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

print(pytesseract.image_to_string(name_img, config="--psm 7").strip())
print(50 * "-")
print(pytesseract.image_to_string(mana_img).strip())  # mana won't work with OCR probably
print(50 * "-")
print(pytesseract.image_to_string(type_img, config="--psm 7").strip())
print(50 * "-")
print(pytesseract.image_to_string(description_img, config="--psm 6").strip())
print(50 * "-")
print(pytesseract.image_to_string(power_img, config="--psm 7").strip())

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
