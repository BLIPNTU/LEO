FIXED_LANGUAGES = {"English", "Tamil", "Malay", "Mandarin"}
CN_DIALECTS = ['Cantonese', 'Hainanese', 'Hakka', 'Henghua', 'Hokchew',
               'Hokchia', 'Hokkien', 'Jiangxi', 'Shanghainese', 'Sichuan', 'Teochew']
BAHASA_DIALECTS = ['Bahasa Indonesia', 'Javanese', 'Boyanese', 'Malaysian Dialect', 'Other Bahasa']
INDIAN_DIALECTS = ['Bengali', 'Gujarati', 'Hindi', 'Punjabi', 'Urdu', 'Malayalam', "Telugu"]
CN_DIALECT_COLORS = ['#FF7518', '#E69F00', '#FF9966', '#FFCC99']
BAHASA_DIALECT_COLORS = ['#336633', '#009933']
INDIAN_DIALECT_COLORS = ["#663399", "#702963"]
OTHER_COLORS = ['#9B111E', '#999999', '#996515', '#000080', '#FF0000', '#6F4E37', '#636C77', '#C21E56', '#1C39BB', '#464647', '#5B342E']
COLOR_MAP = {
    'English': '#0072B2',
    'Mandarin': '#D55E00',
    'Malay': '#009E73',
    'Tamil': '#CC79A7',
    'Arabic': '#F0E442'
}
COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00',
          '#FF9966', '#FFCC99', '#336633', '#009933', '#663399',
          '#53239A', '#F0E442', '#999999']


def map_language(language, prev_languages, color_options, reuse_lastcolor=False):
    if len(prev_languages) < len(color_options):
        color = color_options[len(prev_languages)]
        prev_languages.append(language)
    elif reuse_lastcolor:
        return color_options[-1]
    else:
        color = None
    return color


def to_color_list(languages, reuse_lastcolor=False):
    color_list = []
    _bahasa_dialects = []
    _cn_dialects = []
    _indian_dialects = []
    _others = []
    for language in (x.strip().title() for x in languages):
        color = None
        if language in COLOR_MAP:
            color = COLOR_MAP[language]
        elif language in CN_DIALECTS:
            color = map_language(language, _cn_dialects, CN_DIALECT_COLORS)
        elif language in BAHASA_DIALECTS:
            color = map_language(language, _bahasa_dialects, BAHASA_DIALECT_COLORS)
        elif language in INDIAN_DIALECTS:
            color = map_language(language, _indian_dialects, INDIAN_DIALECT_COLORS)
        if color is None:
            color = map_language(language, _others, OTHER_COLORS, reuse_lastcolor=reuse_lastcolor)
        if color is None:
            raise Exception("There are not enough colours to choose from")
        color_list.append(color)
    return color_list
