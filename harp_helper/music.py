"""
music.py - General music functions
"""
import logging
import re

FLAT_NOTE_ORDER = ("c", "des", "d", "ees", "e", "f", "ges", "g", "aes", "a", "bes", "b")
SHARP_NOTE_ORDER = ("c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b")
PIPE_NOTATION = (",,,", ",,", ",", "", "'", "''", "'''", "''''", "'''''", "''''''")
SCALES = {
    'c': ('c', 'd', 'e', 'f', 'g', 'a', 'b'),
    'des': ('des', 'ees', 'f', 'ges', 'aes', 'bes', 'c'),
    'd': ('d', 'e', 'fis', 'g', 'a', 'b', 'cis'),
    'ees': ('ees', 'f', 'ges', 'aes', 'bes', 'c', 'd'),
    'e': ('e', 'fis', 'gis', 'a', 'b', 'cis', 'dis'),
    'f': ('f', 'g', 'a', 'bes', 'c', 'd', 'e'),
    'fis': ('fis', 'gis', 'ais', 'b', 'cis', 'dis', 'eis'),
    'g': ('g', 'a', 'b', 'c', 'd', 'e', 'fis'),
    'aes': ('aes', 'bes', 'c', 'des', 'ees', 'f', 'g'),
    'a': ('a', 'b', 'cis', 'd', 'e', 'fis', 'gis'),
    'bes': ('bes', 'c', 'd', 'ees', 'f', 'g', 'a'),
    'b': ('b', 'cis', 'dis', 'e', 'fis', 'gis', 'ais')
}
KEYS = list(SCALES.keys())
SCALE_STEPS = (2, 2, 1, 2, 2, 2, 1)

# Build Chromatic scales  programmatically
CHROMATICS = {}
CHROMATIC_INDEX = {}


def build_chromatic_scales():
    """Temporary function to build chromatic scales programmatically"""
    for accidental, order in {'es': FLAT_NOTE_ORDER, 'is': SHARP_NOTE_ORDER}.items():
        CHROMATICS[accidental] = {}
        CHROMATIC_INDEX[accidental] = {}
        index = 0
        for octave in PIPE_NOTATION:
            for note in order:
                CHROMATICS[accidental][note + octave] = index
                CHROMATIC_INDEX[accidental][index] = note + octave
                index += 1


build_chromatic_scales()
del build_chromatic_scales


def get_major_scale(key, by_index: bool = False):

    def index_generator(starting_note):
        index = find_note_index(starting_note)
        while True:
            for steps in SCALE_STEPS:
                yield index
                index += steps

    scale = SCALES[key]
    notes = {}

    # Handle first octave
    octave = PIPE_NOTATION[0]
    index_gen = index_generator(key + octave)
    for letter in scale[scale.index(key):]:
        if by_index:
            notes[index_gen.__next__()] = letter + octave
        else:
            notes[letter + octave] = index_gen.__next__()

    # Remaining octaves
    for octave in PIPE_NOTATION[1:]:
        for letter in scale:
            if by_index:
                notes[index_gen.__next__()] = letter + octave
            else:
                notes[letter + octave] = index_gen.__next__()

    return notes


def find_note_indices(notation: str) -> list[int]:
    indices = []
    for note in notation.strip().split():
        if note in CHROMATICS['es']:
            indices.append(CHROMATICS['es'][note])
        elif note in CHROMATICS['is']:
            indices.append(CHROMATICS['is'][note])
        else:
            raise ValueError(f"Notation '{notation}' is invalid")
    return indices


def find_note_index(notation: str) -> int:
    values = find_note_indices(notation)
    if len(values) != 1:
        raise ValueError(f"Notation '{notation}' is not valid")
    return values[0]

def get_key_from_control_string(control_string: str):

    if not (match := re.search(r"^\s*(\S+)\s+\\(\S+)", control_string)):
        return None


class NoteParser:

    note_regex = re.compile(r"^([a-g])(es|is|)('+|,+|)(\d*\.?)$")
    sf_symbol = {'es': 'b', 'is': '#', '': ''}

    def __init__(self, notation: str):
        self.notation = notation.strip().lower()
        match = self.note_regex.search(self.notation)
        if not match:
            raise ValueError(f"Notation '{notation}' is invalid")
        self.letter, self.accidental, self.octave, self.value = match.groups()

    @property
    def generic_name(self):
        return self.letter + self.accidental

    @property
    def musical_name(self):
        return f"{self.letter.upper()}{self.sf_symbol[self.accidental]}"

    @property
    def is_sharp(self):
        if self.accidental == "is":
            return True
        return False

    @property
    def is_flat(self):
        if self.accidental == "es":
            return True
        return False

    @property
    def is_natural(self):
        if self.accidental == "":
            return True
        return False


class KeySignature:

    def __init__(self, notation: str):
        self._note_parser = NoteParser(notation)
        self.scale_by_index = get_major_scale(notation, by_index=True)
        if self._note_parser.generic_name not in KEYS:
            raise ValueError(f"Unsupported key signature {notation}. must be one of {KEYS}")

    @property
    def key(self):
        """Gets the key in notation format"""
        return self.chromatic_index[self.index]

    @key.setter
    def key(self, notation):
        """Sets the key in notation format"""
        self._note_parser = NoteParser(notation)

    @property
    def index(self) -> int:
        try:
            return KEYS.index(self._note_parser.generic_name)
        except ValueError:
            raise ValueError(f"Key index not found in {KEYS}") from None

    @property
    def name(self):
        return self._note_parser.musical_name

    @property
    def notation(self):
        return self._note_parser.notation

    @property
    def is_flat(self) -> bool:
        if self._note_parser.accidental == "es" \
                or (self._note_parser.letter == "f" and self._note_parser.accidental == ""):
            return True
        return False

    @property
    def is_sharp(self) -> bool:
        return not self.is_flat

    @property
    def scale(self):
        if self.is_flat:
            return "es"
        return "is"

    @property
    def chromatic_scale(self):
        return CHROMATICS[self.scale]

    @property
    def chromatic_index(self):
        return CHROMATIC_INDEX[self.scale]

    @staticmethod
    def get_note_index(notation):
        """Returns the index of a note from the chromatic scale"""
        return find_note_index(notation)

    def get_scale_notation(self, index: int):
        return self.scale_by_index.get(index, self.get_note_notation(index))

    def get_note_notation(self, index: int):
        """Returns the notation of a note from the chromatic scale"""
        try:
            return self.chromatic_index[index]
        except KeyError:
            raise ValueError(f"Invalid index {index}") from None

    def get_transposition_half_steps(self, to_key, direction: (None, str) = None):

        new_key = KeySignature(to_key)
        delta = new_key.index - self.index
        if new_key.index > self.index:
            up = delta
            down = delta - len(KEYS)
        else:
            down = delta
            up = len(KEYS) + delta
        if direction == "up":
            return up
        elif direction == "down":
            return down
        if abs(up) < abs(down):
            return up
        return down

    def __int__(self) -> int:
        return self.index

    def __gt__(self, other):
        if self.index > other.index:
            return True
        return False

    def __lt__(self, other):
        if self.index < other.index:
            return True
        return False

    def __eq__(self, other):
        if self.index == other.index:
            return True
        return False

    def __repr__(self):
        return self.index

    def __str__(self):
        return self.name


class MusicExpression:

    def __init__(self, notation: str, key: str):
        self.logger = logging.getLogger(__name__)
        self._key: KeySignature = KeySignature(key)
        self._notes: list[int] = find_note_indices(notation)
        self.logger.debug(f"loaded notation='{notation}', key={key}")

    def transpose_half_steps(self, steps):
        self.logger.debug(f"transposing half-steps={steps}")
        for index in range(len(self._notes)):
            self._notes[index] += steps
            if self._notes[index] < 0 or self._notes[index] not in self._key.chromatic_index:
                raise ValueError("Transposition is out of range")

    def transpose_to_key(self, key: str, direction: (None, str) = None):
        self.logger.debug(f"transposing key from {self.key} to {key}")
        self.transpose_half_steps(self._key.get_transposition_half_steps(key, direction))
        self._key = KeySignature(key)

    @property
    def key(self):
        return self._key.key

    @property
    def notation(self) -> str:
        """notation as a single string"""
        return " ".join(self.notation_list)

    @property
    def notation_list(self) -> list[str]:
        """List of strings - each note in notation form"""
        return [self._key.chromatic_index[n] for n in self._notes]

    @property
    def scale_notation_list(self) -> list[str]:
        return [self._key.get_scale_notation(index) for index in self._notes]
