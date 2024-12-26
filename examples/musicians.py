from ismain import is_main

from dictim import dictim


def musicians():
    # keys with various cases (values remain the same)
    favorites = dictim({"Hamm": "bass", "Skolnick": "guitar", "Björk": "vocal", "MOTÖRHEAD": "band", "Anne-Sophie Mutter": "Violin", "Strauß": "composer"})
    print("given:")
    for artist, kind in favorites.items():
        print(f" {artist}: {kind}")
    print()

    # access values with different cases than the original dictim, including Unicode
    print("using different case keys than the given mapping:")
    for artist in ["HAMM", "skolnick", "BJÖRK", "MotörHead", "Anne-sophie MUTTER", "StrauSS"]:
        kind = favorites[artist]
        print(f" {artist}: {kind}")
    print()

    print('"in" is also case-insensitive and case fold:')
    print(f' {"haMM" in favorites=}')
    print(f' {"Strauss" in favorites=}')


if is_main():
    musicians()
