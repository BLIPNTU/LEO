import json
import math
import logging
from chirptext import DataObject as DObj
from chirptext import chio
from chirptext.leutile import hamilton_allocate
from .colors import to_color_list, FIXED_LANGUAGES


def getLogger():
    return logging.getLogger(__name__)


class SkillMatrix:
    def __init__(self, understanding, reading, writing, speaking, max_value=10):
        self.understanding = understanding
        self.reading = reading
        self.writing = writing
        self.speaking = speaking
        self.max_value = max_value

    @property
    def max_value(self):
        return self.__max_value

    @max_value.setter
    def max_value(self, value):
        if value is not None and value <= 0:
            raise Exception("Max value of a skill matrix must be positive")
        self.__max_value = value
        
    @property
    def top(self):
        return self.understanding

    @property
    def right(self):
        return self.reading

    @property
    def bottom(self):
        return self.writing
    
    @property
    def left(self):
        return self.speaking

    def to_tuple(self):
        return (self.understanding, self.reading, self.writing, self.speaking)

    def __iter__(self):
        return iter(self.to_tuple())

    def __repr__(self):
        return str((self.understanding, self.reading, self.writing, self.speaking))

    def is_valid(self, strict=True):
        if strict:
            MIN = 0
        else:
            MIN = -1  # allow missing values
        if self.understanding >= MIN and self.reading >= MIN and self.writing >= MIN and self.speaking >= MIN:
            if self.max_value:
                return self.understanding <= self.max_value and self.reading <= self.max_value and self.writing <= self.max_value and self.speaking <= self.max_value
            else:
                return True
        return False

    def __str__(self):
        return repr(self)


class LEOPerson(DObj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.languages = dict()

    def validate(self, messages=None, require_matrix=True, strict=True, hamilton=False):
        if messages is None:
            messages = []
        dist_sum = 0
        _myname = self.name.upper() if self.name else '<<UNKNOWN PERSON>>'
        if not self.name:
            messages.append("There is a person without name")
        for langname, lang in self.languages.items():
            if lang.dist == -1 and strict:
                messages.append(f"lang dist score of {_myname} - language: {langname} is negative")
            elif lang.dist > 100:
                messages.append(f"lang dist score of {_myname} - language: {langname} is {lang.dist} (> 100)")
            dist_sum += lang.dist
            if require_matrix and not lang.skills.is_valid(strict=strict):
                lang_tuple = lang.skills.to_tuple()
                if lang_tuple == (-1, -1, -1, -1):
                    messages.append(f"{_myname} does not have a spider chart")
                else:
                    messages.append(f"SkillMatrix of {_myname} contains invalid value(s) -> {lang_tuple}")
        if not len(self.languages):
            messages.append(f"{_myname} does not have language info (language name, scores, etc.)")
        if not math.isclose(dist_sum, 100.0):
            lang_dists = [str(lang.dist) for lang in self.languages.values()]
            if hamilton:
                getLogger().warning(f"  -- Language skill of {_myname} does not sum up to 100%  |  {' + '.join(lang_dists)} = {dist_sum}")
                lang_keys = self.languages.keys()
                old_values = [self.languages[k].dist for k in lang_keys]
                new_values = hamilton_allocate(old_values)
                for k, v in zip(lang_keys, new_values):
                    self.languages[k].dist = v
                getLogger().warning(f"  -- Fixed using Hamilton method to: {lang_keys} | {new_values}")
            else:
                messages.append(f"Language skill of {_myname} does not sum up to 100%  |  {' + '.join(lang_dists)} = {dist_sum}")
        return messages

    def to_dict(self):
        a_dict = super().to_dict()
        language_matrix = []
        for k, v in self.languages.items():
            language_matrix.append((k, v.dist, *v.skills))
        a_dict['languages'] = language_matrix
        return a_dict

    @staticmethod
    def from_dict(a_dict):
        person = LEOPerson(**a_dict)
        person.languages.update({x[0]: LanguageSkill(x[1], x[2:]) for x in a_dict['languages']})
        return person


class LanguageSkill(DObj):
    def __init__(self, dist, skills, **kwargs):
        """ A person's language skills (understanding, reading, writing, speaking)  """
        super().__init__(dist=dist, skills=SkillMatrix(*skills), **kwargs)


class LEOProfile(DObj):
    def __init__(self, reportID, *args, languages=None, **kwargs):
        """
        LEO Profile Data Structure
        """
        super().__init__(reportID=reportID, **kwargs)
        if languages is None:
            self.languages = []
        else:
            self.languages = [l for l in languages if l not in FIXED_LANGUAGES]

    def output_filename(self):
        if self.pdf_filename:
            return self.pdf_filename
        elif self.reportID:
            return f"{self.reportID}.pdf"
        else:
            return "report.pdf"

    def to_dict(self):
        a_dict = super().to_dict()
        a_dict['baby'] = self.baby.to_dict()
        a_dict['people'] = [p.to_dict() for p in self.people]
        return a_dict

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)

    def gather_languages(self):
        languages = {k for k, v in self.baby.languages.items()}
        languages.update(self.languages)
        for person in self.people:
            languages.update(k for k, v in person.languages.items())
        return languages

    def get_extra_language_legends(self, limit=4):
        return [l for l in self.gather_languages() if l not in FIXED_LANGUAGES][:limit]

    def build_language_color_map(self):
        languages = self.gather_languages()
        colors = to_color_list(languages)
        return {l: c for l, c in zip(languages, colors)}

    def validate(self, strict=True, require_matrix=True, hamilton=False):
        messages = []
        if not self.reportID or not str(self.reportID).strip():
            messages.append("ReportID cannot be empty")
        if not self.baby.name:
            messages.append("Baby name is empty")
        if not self.baby.age:
            messages.append("Baby age is empty")
        if not self.baby.languages:
            messages.append("Baby language info is missing")
        else:
            self.baby.validate(messages, require_matrix=False, strict=strict, hamilton=hamilton)
        for person in self.people:
            person.validate(messages, require_matrix=require_matrix, strict=strict, hamilton=hamilton)
        return messages

    @staticmethod
    def from_dict(a_dict):
        reportID = ''
        kwargs = {}
        for k, v in a_dict.items():
            if k == 'reportID':
                reportID = v
            elif k == 'cert_date':
                kwargs['cert_date'] = v
            elif k == 'pdf_filename':
                kwargs[k] = v
            else:
                if k == 'baby':
                    v = LEOPerson.from_dict(v)
                elif k == 'people':
                    v = [LEOPerson.from_dict(p) for p in v]
                kwargs[k] = v
        return LEOProfile(reportID, **kwargs)

    @staticmethod
    def from_json_str(json_string):
        return LEOProfile.from_dict(json.loads(json_string))

    @staticmethod
    def from_file(input_path):
        return LEOProfile.from_json_str(chio.read_file(input_path))


def read_json(input_path):
    return LEOProfile.from_file(input_path)
