# Language Experience Overview (LEO) Report Generator

`blipleo` is a Python package to generate Language Experience Overview (LEO) report.


## Installation

`blipleo` package is available on PyPI and can be installed using pip

```bash
pip install blipleo
```

To generate a LEO report, prepare a json data file (See `data/baby_test.json` in `blipleo`'s source code repository)
and use the following commands:

```python
import blipleo
leo = blipleo.read_json('./data/baby_test.json')
blipleo.generate_leo(leo, './data')
```

## License

- The blipleo package is licensed under GPL version 3.0
- The LEO template graphic vector files under templates folder are licensed under CC-BY-NC 4.0

## Contact

For more information, please contact Fei Ting Woon at feitingwoon@ntu.edu.sg
