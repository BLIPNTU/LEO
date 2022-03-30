# Language Experience Overview (LEO) Report Generator

[![Total alerts](https://img.shields.io/lgtm/alerts/g/BLIPNTU/LEO.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BLIPNTU/LEO/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BLIPNTU/LEO.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BLIPNTU/LEO/context:python)

In Singapore, more than 90% of adults are literate in at least 2 languages (Singapore Census, 2010). 
Singaporean families often involve grandparents in the care of young children, and one in five families employ a live-in foreign worker for domestic help (Singapore Ministry of Manpower, 2020). 
Infants in Singapore typically hear two or more languages from each parent, two-to-three languages from their grandparents (Woon, 2018), and possibly more from a domestic helper. 
Given this complexity, existing models of balanced/unbalanced or dominant/non-dominant bilingualism are insufficient for describing the rich tapestry of multilingual experiences. 
In order to capture this variety, we created a flexible multilingual tool, the Language Experience Overview (LEO). 
This multivariate multilingual tool combines estimates of care time and language-use ratios with language profiles of each caregiver. 
Importantly, the LEO Report visualises the results in parent-friendly feedback. 

`blipleo` is a Python package to generate Language Experience Overview (LEO) report.

Citation: 
Woon, Fei Ting; Le, Tuan Anh; binte Amran, Shaza; Ang, Wen Xin; Styles, Suzy J, 2021, "Language Experiences Overview (LEO)", https://doi.org/10.21979/N9/XQUFEW, DR-NTU (Data), V1

## Installation

`blipleo` package is available on the Python official package index PyPI: https://pypi.org/project/blipleo/

It can be installed on Python 3.6 or later using pip

```bash
pip install blipleo
```

**Notes:** `blipleo` requires [Inkscape](https://inkscape.org/release/) to generate PDF files, which can be downloaded freely at https://inkscape.org/release/

## Usage

To generate a LEO report, prepare a LEO json data file (For sample see: [data/baby_test.json](https://github.com/BLIPNTU/LEO/blob/main/data/baby_test.json))
and use the following commands:

```python
import blipleo
leo = blipleo.read_json('./data/baby_test.json')
blipleo.generate_leo(leo, './data')
```

The generated LEO report looks like this: https://github.com/BLIPNTU/LEO/blob/main/data/baby_test.pdf

## License

- The blipleo package is licensed under GPL version 3.0
- The LEO template graphic vector files under templates folder are licensed under CC-BY-NC 4.0

## Developers

- `blipleo` is a free software, source code is available on Github: https://github.com/BLIPNTU/LEO
- LEO research archive: https://doi.org/10.21979/N9/XQUFEW
- Maintainer: [Le Tuan Anh](https://github.com/letuananh)

## Contact

For more information, please contact Fei Ting Woon at feitingwoon@ntu.edu.sg
