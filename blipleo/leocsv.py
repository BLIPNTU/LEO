import logging
import json
from chirptext import chio

from .models import FIXED_LANGUAGES, LEOProfile
# LEO old CSV fields
SPIDER_FIELDS = ['name of child', 'age', 'mother_english_speaking', 'mother_english_understanding', 'mother_english_reading', 'mother_english_writing', 'mother_mandarin_speaking', 'mother_mandarin_understanding', 'mother_mandarin_reading', 'mother_mandarin_writing', 'mother_ malay_speaking', 'mother_malay_understanding', 'mother_malay_reading', 'mother_malay_writing', 'mother_tamil_speaking', 'mother_tamil_understanding', 'mother_tamil_reading', 'mother_tamil_writing', 'mother_other1_text', 'mother_other1_speaking', 'mother_other1_understanding', 'mother_other1_reading', 'mother_other1_writing', 'mother_other2_text', 'mother_other2_speaking', 'mother_other2_understanding', 'mother_other2_reading', 'mother_other2_writing', 'mother_other3_text', 'mother_other3_speaking', 'mother_other3_understanding', 'mother_other3_reading', 'mother_other3_writing', 'mother_other4_text', 'mother_other4_speaking', 'mother_other4_understanding', 'mother_other4_reading', 'mother_other4_writing', '', 'father_english_speaking', 'father_english_understanding', 'father_english_reading', 'father_english_writing', 'father_mandarin_speaking', 'father_mandarin_understanding', 'father_mandarin_reading', 'father_mandarin_writing', 'father_ malay_speaking', 'father_malay_understanding', 'father_malay_reading', 'father_malay_writing', 'father_tamil_speaking', 'father_tamil_understanding', 'father_tamil_reading', 'father_tamil_writing', 'father_other1_text', 'father_other1_speaking', 'father_other1_understanding', 'father_other1_reading', 'father_other1_writing', 'father_other2_text', 'father_other2_speaking', 'father_other2_understanding', 'father_other2_reading', 'father_other2_writing', 'father_other3_text', 'father_other3_speaking', 'father_other3_understanding', 'father_other3_reading', 'father_other3_writing', 'father_other4_text', 'father_other4_speaking', 'father_other4_understanding', 'father_other4_reading', 'father_other4_writing', 'caregiver1_text', 'caregiver1_english_speaking', 'caregiver1_english_understanding', 'caregiver1_english_reading', 'caregiver1_english_writing', 'caregiver1_mandarin_speaking', 'caregiver1_mandarin_understanding', 'caregiver1_mandarin_reading', 'caregiver1_mandarin_writing', 'caregiver1_ malay_speaking', 'caregiver1_malay_understanding', 'caregiver1_malay_reading', 'caregiver1_malay_writing', 'caregiver1_tamil_speaking', 'caregiver1_tamil_understanding', 'caregiver1_tamil_reading', 'caregiver1_tamil_writing', 'caregiver1_other1_text', 'caregiver1_other1_speaking', 'caregiver1_other1_understanding', 'caregiver1_other1_reading', 'caregiver1_other1_writing', 'caregiver1_other2_text', 'caregiver1_other2_speaking', 'caregiver1_other2_understanding', 'caregiver1_other2_reading', 'caregiver1_other2_writing', 'caregiver1_other3_text', 'caregiver1_other3_speaking', 'caregiver1_other3_understanding', 'caregiver1_other3_reading', 'caregiver1_other3_writing', 'caregiver1_other4_text', 'caregiver1_other4_speaking', 'caregiver1_other4_understanding', 'caregiver1_other4_reading', 'caregiver1_other4_writing', 'caregiver2_text', 'caregiver2_english_speaking', 'caregiver2_english_understanding', 'caregiver2_english_reading', 'caregiver2_english_writing', 'caregiver2_mandarin_speaking', 'caregiver2_mandarin_understanding', 'caregiver2_mandarin_reading', 'caregiver2_mandarin_writing', 'caregiver2_ malay_speaking', 'caregiver2_malay_understanding', 'caregiver2_malay_reading', 'caregiver2_malay_writing', 'caregiver2_tamil_speaking', 'caregiver2_tamil_understanding', 'caregiver2_tamil_reading', 'caregiver2_tamil_writing', 'caregiver2_other1_text', 'caregiver2_other1_speaking', 'caregiver2_other1_understanding', 'caregiver2_other1_reading', 'caregiver2_other1_writing', 'caregiver2_other2_text', 'caregiver2_other2_speaking', 'caregiver2_other2_understanding', 'caregiver2_other2_reading', 'caregiver2_other2_writing', 'caregiver2_other3_text', 'caregiver2_other3_speaking', 'caregiver2_other3_understanding', 'caregiver2_other3_reading', 'caregiver2_other3_writing', 'caregiver2_other4_text', 'caregiver2_other4_speaking', 'caregiver2_other4_understanding', 'caregiver2_other4_reading', 'caregiver2_other4_writing', 'caregiver3_text', 'caregiver3_english_speaking', 'caregiver3_english_understanding', 'caregiver3_english_reading', 'caregiver3_english_writing', 'caregiver3_mandarin_speaking', 'caregiver3_mandarin_understanding', 'caregiver3_mandarin_reading', 'caregiver3_mandarin_writing', 'caregiver3_ malay_speaking', 'caregiver3_malay_understanding', 'caregiver3_malay_reading', 'caregiver3_malay_writing', 'caregiver3_tamil_speaking', 'caregiver3_tamil_understanding', 'caregiver3_tamil_reading', 'caregiver3_tamil_writing', 'caregiver3_other1_text', 'caregiver3_other1_speaking', 'caregiver3_other1_understanding', 'caregiver3_other1_reading', 'caregiver3_other1_writing', 'caregiver3_other2_text', 'caregiver3_other2_speaking', 'caregiver3_other2_understanding', 'caregiver3_other2_reading', 'caregiver3_other2_writing', 'caregiver3_other3_text', 'caregiver3_other3_speaking', 'caregiver3_other3_understanding', 'caregiver3_other3_reading', 'caregiver3_other3_writing', 'caregiver3_other4_text', 'caregiver3_other4_speaking', 'caregiver3_other4_understanding', 'caregiver3_other4_reading', 'caregiver3_other4_writing', 'caregiver4_text', 'caregiver4_english_speaking', 'caregiver4_english_understanding', 'caregiver4_english_reading', 'caregiver4_english_writing', 'caregiver4_mandarin_speaking', 'caregiver4_mandarin_understanding', 'caregiver4_mandarin_reading', 'caregiver4_mandarin_writing', 'caregiver4_ malay_speaking', 'caregiver4_malay_understanding', 'caregiver4_malay_reading', 'caregiver4_malay_writing', 'caregiver4_tamil_speaking', 'caregiver4_tamil_understanding', 'caregiver4_tamil_reading', 'caregiver4_tamil_writing', 'caregiver4_other1_text', 'caregiver4_other1_speaking', 'caregiver4_other1_understanding', 'caregiver4_other1_reading', 'caregiver4_other1_writing', 'caregiver4_other2_text', 'caregiver4_other2_speaking', 'caregiver4_other2_understanding', 'caregiver4_other2_reading', 'caregiver4_other2_writing', 'caregiver4_other3_text', 'caregiver4_other3_speaking', 'caregiver4_other3_understanding', 'caregiver4_other3_reading', 'caregiver4_other3_writing', 'caregiver4_other4_text', 'caregiver4_other4_speaking', 'caregiver4_other4_understanding', 'caregiver4_other4_reading', 'caregiver4_other4_writing', 'caregiver5_text', 'caregiver5_english_speaking', 'caregiver5_english_understanding', 'caregiver5_english_reading', 'caregiver5_english_writing', 'caregiver5_mandarin_speaking', 'caregiver5_mandarin_understanding', 'caregiver5_mandarin_reading', 'caregiver5_mandarin_writing', 'caregiver5_ malay_speaking', 'caregiver5_malay_understanding', 'caregiver5_malay_reading', 'caregiver5_malay_writing', 'caregiver5_tamil_speaking', 'caregiver5_tamil_understanding', 'caregiver5_tamil_reading', 'caregiver5_tamil_writing', 'caregiver5_other1_text', 'caregiver5_other1_speaking', 'caregiver5_other1_understanding', 'caregiver5_other1_reading', 'caregiver5_other1_writing', 'caregiver5_other2_text', 'caregiver5_other2_speaking', 'caregiver5_other2_understanding', 'caregiver5_other2_reading', 'caregiver5_other2_writing', 'caregiver5_other3_text', 'caregiver5_other3_speaking', 'caregiver5_other3_understanding', 'caregiver5_other3_reading', 'caregiver5_other3_writing', 'caregiver5_other4_text', 'caregiver5_other4_speaking', 'caregiver5_other4_understanding', 'caregiver5_other4_reading', 'caregiver5_other4_writing', 'caregiver6_text', 'caregiver6_english_speaking', 'caregiver6_english_understanding', 'caregiver6_english_reading', 'caregiver6_english_writing', 'caregiver6_mandarin_speaking', 'caregiver6_mandarin_understanding', 'caregiver6_mandarin_reading', 'caregiver6_mandarin_writing', 'caregiver6_ malay_speaking', 'caregiver6_malay_understanding', 'caregiver6_malay_reading', 'caregiver6_malay_writing', 'caregiver6_tamil_speaking', 'caregiver6_tamil_understanding', 'caregiver6_tamil_reading', 'caregiver6_tamil_writing', 'caregiver6_other1_text', 'caregiver6_other1_speaking', 'caregiver6_other1_understanding', 'caregiver6_other1_reading', 'caregiver6_other1_writing', 'caregiver6_other2_text', 'caregiver6_other2_speaking', 'caregiver6_other2_understanding', 'caregiver6_other2_reading', 'caregiver6_other2_writing', 'caregiver6_other3_text', 'caregiver6_other3_speaking', 'caregiver6_other3_understanding', 'caregiver6_other3_reading', 'caregiver6_other3_writing', 'caregiver6_other4_text', 'caregiver6_other4_speaking', 'caregiver6_other4_understanding', 'caregiver6_other4_reading', 'caregiver6_other4_writing']
PIE_FIELDS = ['name of child', 'mother_aveweekday', 'father_aveweekday', 'caregiver1_text', 'caregiver_aveweekday', 'caregiver2_text', 'caregiver2_aveweekday', 'caregiver3_text', 'caregiver3_aveweekday', 'caregiver4_text', 'caregiver4_aveweekday', 'caregiver5_text', 'caregiver5_aveweekday', 'caregiver6_text', 'caregiver6_aveweekday', 'mother_weightedweekday', 'father_weightedweekday', 'caregiver_weightedweekday', 'caregiver2_weightedweekday', 'caregiver3_weightedweekday', 'caregiver4_weightedweekday', 'caregiver5_weightedweekday', 'caregiver6_weightedweekday', 'mother_aveweekend', 'father_aveweekend', 'caregivera_text', 'caregiver_aveweekend', 'caregiverb_text', 'caregiver2_aveweekend', 'caregiverc_text', 'caregiver3_aveweekend', 'caregiverd_text', 'caregiver4_aveweekend', 'caregivere_text', 'caregiver5_aveweekend', 'caregiverf_text', 'caregiver6_aveweekend', 'mother_weightedweekend', 'father_weightedweekend', 'caregivera_weightedweekend', 'caregiverb_weightedweekend', 'caregiverc_weightedweekend', 'caregiverd_weightedweekend', 'caregivere_weightedweekend', 'caregiverf_weightedweekend', 'mother_totalweighted', 'father_totalweighted', '', 'caregiver11_totalweighted', 'caregiver21_totalweighted', 'caregiver31_totalweighted', 'caregiver41_totalweighted', 'caregiver51_totalweighted', 'caregiver61_totalweighted', 'mother_prop', 'father_prop', 'caregiver11_proportion', 'caregiver21_prop', 'caregiver31_prop', 'caregiver41_prop', 'caregiver51_prop', 'caregive61_prop', 'mother_english_input', 'mother_mandarin_input', 'mother_malay_input', 'mother_tamil_input', 'mother_other1_text', 'mother_other1_input', 'mother_other2_text', 'mother_other2_input', 'mother_other3_text', 'mother_other3_input', 'mother_other4_text', 'mother_other4_input', 'father_english_input', 'father_mandarin_input', 'father_malay_input', 'father_tamil_input', 'father_other1_text', 'father_other1_input', 'father_other2_text', 'father_other2_input', 'father_other3_text', 'father_other3_input', 'father_other4_text', 'father_other4_input', 'caregiver11_text', 'caregiver11_english_input', 'caregiver11_mandarin_input', 'caregiver11_malay_input', 'caregiver11_tamil_input', 'caregiver11_other1_text', 'caregiver11_other1_input', 'caregiver11_other2_text', 'caregiver11_other2_input', 'caregiver11_other3_text', 'caregiver11_other3_input', 'caregiver11_other4_text', 'caregiver11_other4_input', 'caregiver21_text', 'caregiver21_english_input', 'caregiver21_mandarin_input', 'caregiver21_malay_input', 'caregiver21_tamil_input', 'caregiver21_other1_text', 'caregiver21_other1_input', 'caregiver21_other2_text', 'caregiver21_other2_input', 'caregiver21_other3_text', 'caregiver21_other3_input', 'caregiver21_other4_text', 'caregiver21_other4_input', 'caregiver31_text', 'caregiver31_english_input', 'caregiver31_mandarin_input', 'caregiver31_malay_input', 'caregiver31_tamil_input', 'caregiver31_other1_text', 'caregiver31_other1_input', 'caregiver31_other2_text', 'caregiver31_other2_input', 'caregiver31_other3_text', 'caregiver31_other3_input', 'caregiver31_other4_text', 'caregiver31_other4_input', 'caregiver41_text', 'caregiver41_english_input', 'caregiver41_mandarin_input', 'caregiver41_malay_input', 'caregiver41_tamil_input', 'caregiver41_other1_text', 'caregiver41_other1_input', 'caregiver41_other2_text', 'caregiver41_other2_input', 'caregiver41_other3_text', 'caregiver41_other3_input', 'caregiver41_other4_text', 'caregiver41_other4_input', 'caregiver51_text', 'caregiver51_english_input', 'caregiver51_mandarin_input', 'caregiver51_malay_input', 'caregiver51_tamil_input', 'caregiver51_other1_text', 'caregiver51_other1_input', 'caregiver51_other2_text', 'caregiver51_other2_input', 'caregiver51_other3_text', 'caregiver51_other3_input', 'caregiver51_other4_text', 'caregiver51_other4_input', 'caregiver61_text', 'caregiver61_english_input', 'caregiver61_mandarin_input', 'caregiver61_malay_input', 'caregiver61_tamil_input', 'caregiver61_other1_text', 'caregiver61_other1_input', 'caregiver61_other2_text', 'caregiver61_other2_input', 'caregiver61_other3_text', 'caregiver61_other3_input', 'caregiver61_other4_text', 'caregiver61_other4_input', 'english_total', 'mandarin_total', 'malay_total', 'tamil_total', 'other1_text', 'other1_total', 'other2_text', 'other2_total', 'other3_text', 'other3_total', 'other4_text', 'other4_total', 'sum_check', '']


def getLogger():
    return logging.getLogger(__name__)


def validate_fields(expected, actual, message="Invalid fields"):
    if expected != actual:
        raise Exception(message)
    else:
        return True


class LEOJSONBuilder:
    def __init__(self):
        self.json_data = {"baby": {"languages": []}}
        self.person_dict = {}

    def person(self, key):
        if key not in self.person_dict:
            self.person_dict[key] = {'languages': [], 'name': ''}
        return self.person_dict[key]

    def set(self, key, value):
        if key in self.json_data:
            logging.getLogger(__name__).warning(f"Potential duplicated key: {key} -- [old={self.json_data[key]}, new={value}]")
        self.json_data[key] = value

    def language_row(self, *values):
        try:
            return [values[0]] + [float(values[1])] + [int(x) for x in values[2:]]
        except Exception as e:
            __source = f"reportID={self.json_data['reportID']} " if 'reportID' in self.json_data else ""
            getLogger().exception(f"{__source}Casting: {values[1]} => float -- {values[2:]} => int")
            raise e

    def to_profile(self):
        return LEOProfile.from_dict(self.to_dict())

    def to_dict(self):
        self.json_data['people'] = []
        for pkey in sorted(self.person_dict.keys()):
            self.json_data['people'].append(self.person_dict[pkey])
        return self.json_data

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def save(self, path, *args, **kwargs):
        chio.write_file(path, self.to_json())

    @staticmethod
    def cut_flat_row(row):
        """ Convert Feiting's flat CSV file (1 row per participant) into LEO's CSV files (1 file per participant)
        (i.e. 1 flat-row is 1 multiple-row CSV file) 
        
        The multiple-row format is easier to debug when errors happen.
        It's also closer to the LEO JSON format.
        """
        cut_points = [idx for idx in range(len(row)) if idx in (0, 2) or '__' in row[idx]]
        parts = []
        for idx, c in enumerate(cut_points):
            if idx == len(cut_points) - 1:
                part = row[c:]
            else:
                part = row[c:cut_points[idx + 1]]
            parts.append([x for x in part if x])
        return parts

    @staticmethod
    def from_flat_row(row):
        parts = LEOJSONBuilder.cut_flat_row(row)
        return LEOJSONBuilder.from_rows(parts)

    @staticmethod
    def from_rows(rows):
        """ Create a LEOJSONBuilder from multiple-line CSV format """
        builder = LEOJSONBuilder()
        __source = ""
        for row in rows:
            key = row[0].strip()
            val = row[1].strip()
            if val == '---':
                val = ''
            if key in ('reportID', 'cert__date'):
                if key == 'reportID':
                    __source = f"reportID={val} "
                builder.set(key, row[1].strip())
            elif key == 'languages':
                _langs = [x.strip() for x in row[1:] if x.strip() and x.strip() not in FIXED_LANGUAGES]
                builder.set(key, _langs)
            if key.startswith('baby__'):
                try:
                    key = row[0].strip()[6:]  # baby's subkey
                    if key in ("name", "age"):
                        builder.json_data['baby'][key] = val
                    elif key == 'language':
                        _lang_cols = [_l.strip() for _l in row[1:] if _l.strip()]
                        _langs = [_lang_cols[0]] + [float(_lang_cols[1])] + [int(x) for x in _lang_cols[2:]]
                        builder.json_data['baby']['languages'].append(_langs)
                    else:
                        logging.getLogger(__name__).warning(f"{__source}Invalid baby data key: {row[0]}")
                except Exception:
                    logging.getLogger(__name__).exception(f"{__source}Invalid baby data row: {row}")
            elif row[0].startswith('person__'):
                try:
                    __, key, person_key = row[0].strip().split("__")
                    person = builder.person(person_key)
                    if key == "name":
                        person[key] = row[1].strip()
                    elif key in ("usage", "piesize"):
                        person[key] = float(row[1].strip())
                    elif key == "language":
                        _lang_cols = [_l.strip() for _l in row[1:] if _l.strip()]
                        _langs = [_lang_cols[0]] + [float(_lang_cols[1])] + [int(x) for x in _lang_cols[2:]]
                        if len(_langs) != 6:
                            logging.getLogger(__name__).warnings(f"{__source}[person={person['name']}]Invalid person language: {row}")
                        else:
                            for score in _langs[2:]:
                                if score not in list(range(8)):
                                    logging.getLogger(__name__).warnings(f"{__source}[person={person['name']}]Person language score: {score} must be within the range [0..7]")
                        person["languages"].append(_langs)
                except Exception:
                    logging.getLogger(__name__).exception(f"{__source}Invalid person data row: {row}")
        return builder

    @staticmethod
    def read_csv(csv_file):
        """ Read a multiple-line CSV file """
        rows = chio.read_csv(csv_file, dialect="excel")
        return LEOJSONBuilder.from_rows(rows)


cut_flat_row = LEOJSONBuilder.cut_flat_row
from_flat_row = LEOJSONBuilder.from_flat_row
read_csv = LEOJSONBuilder.read_csv


def make_leo_json(rows):
    """ convert LEO CSV rows to LEO JSON format """
    return LEOJSONBuilder.from_rows(rows).to_json()
