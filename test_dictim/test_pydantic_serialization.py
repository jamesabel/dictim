from pathlib import Path
from pydantic import BaseModel
from typing import List
from decimal import Decimal

from dictim import dictim


class Child(BaseModel):
    name: str
    age: int
    int_key_dict: dictim[int, str]
    my_complex_number: complex = 1 + 2j
    my_decimal: Decimal = Decimal("0.5")


class Parent(BaseModel):
    name: str
    children: List[Child]


def test_pydantic_serialization() -> None:
    # Create a parent instance with nested children
    parent_instance = Parent(
        name="Alice",
        children=[
            Child(name="Bob", age=10, int_key_dict=dictim({1: "one", 2: "two"}), my_complex_number=3 + 4j),
            Child(name="Carol", age=12, int_key_dict=dictim({3: "three", 4: "four"}), my_complex_number=5 + 6j),
        ],
    )

    parent_json: str = parent_instance.model_dump_json(indent=4)

    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True, parents=True)
    output_file: Path = Path(temp_dir, "dictim.json")

    with output_file.open(mode="w", encoding="utf-8") as f:
        f.write(parent_json)

    with output_file.open(mode="r", encoding="utf-8") as f:
        loaded_json = f.read()

    restored_instance: Parent = Parent.model_validate_json(loaded_json)

    assert restored_instance == parent_instance
