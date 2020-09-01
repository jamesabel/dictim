from ismain import is_main

from dictim import dictim


def musicians():
    favorites = dictim({"Hamm": "bass", "Skolnick": "guitar", "Björk": "vocal", "MOTÖRHEAD": "band"})
    # access values with case insensitivity, including unicode
    print(favorites["hamm"])
    print(favorites["skolnick"])
    print(favorites["björk"])
    print(favorites["Motörhead"])


if is_main():
    musicians()
