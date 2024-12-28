# dictim

Case-insensitive `dict` keys. Like a `dict`, but keys are case-insensitive.

- Supports unicode
- Supports pydantic (handy for JSON serialization)

Name comes from `dict`, case-`i`nsensitive, `m`apping.

## Usage

    pip install dictim

# Example

    from dictim import dictim

    favorites = dictim({"Hamm": "bass", "Skolnick": "guitar", "Björk": "vocal", "MOTÖRHEAD": "band"})

    # access values with case insensitivity, including unicode
    print(favorites["hamm"])  # bass
    print(favorites["skolnick"])  # guitar
    print(favorites["björk"])  # vocal
    print(favorites["Motörhead"])  # band
