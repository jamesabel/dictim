# dictim

case insensitive dict for modern Python (Python 3)

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
