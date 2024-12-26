from pydantic import BaseModel, Field

from dictim import dictim


def test_pydantic():
    # ensure dictim can be used as a pydantic field

    class MyModel(BaseModel):
        favorites: dictim = Field(default_factory=dictim)

    favorites = dictim({"Hamm": "bass", "MOTÖRHEAD": "band", "Strauß": "composer"})
    my_model = MyModel(favorites=favorites)
    assert my_model.favorites == {"hamm": "bass", "motörhead": "band", "strauss": "composer"}
