from ismain import is_main
from pydantic import BaseModel, Field

from dictim import dictim


class Musicians(BaseModel):
    favorites: dictim  # must be passed in
    new_wave: dictim = dictim({"Blondie": "band"})  # default from dict
    oldies: dictim = Field(default_factory=dictim)  # no oldies - use default


def main():

    favorites = dictim({"Hamm": "bass", "Björk": "vocal", "MOTÖRHEAD": "band", "Strauß": "composer"})
    musicians = Musicians(favorites=favorites)
    print(musicians)


if is_main():
    main()
