from abc import ABC, abstractmethod
from importlib import import_module
import logging
import pkgutil
import re
from tabulate import tabulate

from harp_helper import music

logger = logging.getLogger(__name__)


class Harmonica(ABC):

    harmonica_type = None
    harmonica_description = "Harmonica"
    keys_available = ("fis", "f", "e", "ees", "d" "des", "c", "b", "bes", "a", "aes", "g")
    action_notation = {}

    def __init__(self, harmonica_type: str, harmonica_key: str = "c"):
        self._key = music.KeySignature(harmonica_key)
        if len(self.action_notation) < 1:
            raise RuntimeError(f"SCRIPT ERROR: action_notation not defined in class {self.get_class_name()}")

    def __new__(cls, harmonica_type: str, harmonica_key: str):
        for subclass in cls.__subclasses__():
            if subclass.harmonica_type == harmonica_type.lower():
                return super(Harmonica, subclass).__new__(subclass)
        raise NotImplementedError(f"Harmonica type {harmonica_type}")

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    @property
    @abstractmethod
    def lowest_note(self):
        pass

    @property
    @abstractmethod
    def highest_note(self):
        pass

    @property
    @abstractmethod
    def tuning_values(self):
        pass

    @classmethod
    def types(cls):
        return {subclass.harmonica_type: subclass.harmonica_description for subclass in cls.__subclasses__()}

    @property
    def flat_key_signature(self) -> bool:
        return self._key.is_flat

    @property
    def sharp_key_signature(self) -> bool:
        return not self.flat_key_signature

    @property
    def name(self):
        return f"{self._key.name} {self.harmonica_description}"

    @staticmethod
    def note_name(key: str) -> str:
        return music.KeySignature(key).name

    def hole_values(self, starting_note: str, intervals: (list[int], tuple[int]), note_order=None) -> list[str]:
        notes = []
        index = self._key.chromatic_scale.get(starting_note)
        if index is None:
            raise ValueError(f"Can't find index for starting note {starting_note}")
        for interval in intervals:
            index += interval
            notes.append(self._key.chromatic_index[index])
        return notes

    def tuning_chart(self,
                     use_music_symbols: bool = True,
                     output_format: str = "table",
                     transpose_steps: int = 0,
                     transpose_key: (None, str) = None):
        """Creates a tuning chart or transposing chart"""

        details = []
        for label, chart_notes in self.tuning_values.items():

            # Process through MusicExpression to handle transposing
            expression = music.MusicExpression(" ".join(chart_notes), key=self._key.notation)
            if transpose_key is not None:
                expression.transpose_to_key(transpose_key)
            if transpose_steps != 0:
                expression.transpose_half_steps(transpose_steps)

            if use_music_symbols:
                details.append([label] + [music.NoteParser(n).musical_name for n in expression.scale_notation_list])
            else:
                details.append([label] + expression.scale_notation_list)

        headers = list(range(1, max([len(line) for line in details])))
        headers.insert(0, "")

        if output_format == "table":
            return tabulate(details, headers=headers, tablefmt="pretty")
        elif output_format == "csv":
            csv_lines = [",".join([str(h) for h in headers])]
            for detail in details:
                csv_lines.append(",".join(detail))
            return "\n".join(csv_lines)
        else:
            raise ValueError(f"Unknown output format {output_format}")

    def get_notation(self, notes: list[str]):
        """"Accepts a list of strings (each note) and outputs list of strings in harmonica tablature """

        holes_by_pitches = {}
        for action, tuning_values in self.tuning_values.items():
            action_format = self.action_notation[action]
            for index in range(len(tuning_values)):
                value = tuning_values[index]
                value_notation = action_format.format(index + 1)
                if value in holes_by_pitches.keys():
                    holes_by_pitches[value] = f"{holes_by_pitches[value]}/{value_notation}"
                else:
                    holes_by_pitches[value] = value_notation

        return [holes_by_pitches.get(n, 'X') for n in notes]


# -------------------------------------------------------------------
# Search through modules in this package for subclasses of Harmonica
# -------------------------------------------------------------------
for mod in [m for m in pkgutil.iter_modules(path=__path__) if not m.name.startswith("_")]:
    import_module(f"{__name__}.{mod.name}")
