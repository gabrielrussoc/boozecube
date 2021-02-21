import xml.etree.ElementTree as ET
from xml.dom import minidom

# Returns a string with the cockatrice database XML
# https://github.com/Cockatrice/Cockatrice/wiki/Custom-Cards-&-Sets
def create_database(all_cards):
    database = ET.Element("cockatrice_carddatabase", {
        "version": "4"
    })

    sets = ET.SubElement(database, "sets")
    set = ET.SubElement(sets, "set")
    set_name = "BC0"  # BoozeCube v0
    ET.SubElement(set, "name").text = set_name
    ET.SubElement(set, "longname").text = "Booze Cube from http://theboozecube.blogspot.com/"
    ET.SubElement(set, "settype").text = "Custom"
    ET.SubElement(set, "releasedate").text = "2021-02-21"

    cards = ET.SubElement(database, "cards")

    for c in all_cards:
        card = ET.SubElement(cards, "card")
        ET.SubElement(card, "name").text = c.name
        ET.SubElement(card, "text").text = c.description

        if c.token:
            ET.SubElement(card, "token").text = "1"

        if c.enters_tapped:
            ET.SubElement(card, "cipt").text = "1"

        ET.SubElement(card, "tablerow").text = tablerow(c.type)

        ET.SubElement(card, "set", {"rarity": rarity(c.rarity), "picurl": c.picurl}).text = set_name

        # TODO: add related tags (which tokens this can create, how many, etc)

        prop = ET.SubElement(card, "prop")
        ET.SubElement(prop, "layout").text = layout(c.layout)
        ET.SubElement(prop, "manacost").text = manacost(c.mana)

        # TODO: add converted mana cost, colors, power/toughness


    return indent(ET.tostring(database))


def indent(xml_str):
    return minidom.parseString(xml_str).toprettyxml(indent="   ")


# TODO: add card type conversion
def tablerow(t):
    return "0"

# TODO: add manacost
def manacost(_):
    return "1W"

# TODO: handle layouts
def layout(l):
    return "normal"

# TODO: handle rarity
def rarity(r):
    return "common"


if __name__ == "__main__":
    from card import Card
    print(create_database([
        Card(
            name="aa",
            description="aa",
            picurl="http://1.bp.blogspot.com/-9_Tv3yunbwU/VnhZYP7Dr4I/AAAAAAAAGDI/4TMvviamoQQ/s1600/Mother%2BBeaver.jpg"
        )
    ]))

