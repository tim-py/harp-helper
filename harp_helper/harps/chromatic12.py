from harp_helper.harps import Harmonica
from harp_helper import music


class Chromatic12(Harmonica):

    harmonica_type = "c12"
    harmonica_description = "Chromatic 12"
    keys_available = ("c", "ees")
    action_notation = {
        "blow >": "{}",
        "draw >": "-{}",
        "blow <": "{}<",
        "draw <": "-{}<"
    }

    @property
    def tuning_values(self):
        return {
            "blow >":  self.hole_values(
                starting_note=self.lowest_note,
                intervals=(0, 4, 3, 5, 0, 4, 3, 5, 0, 4, 3, 5)
            ),
            "draw >":  self.hole_values(
                starting_note=self.lowest_note,
                intervals=(2, 3, 4, 2, 3, 3, 4, 2, 3, 3, 4, 2)
            ),
            "blow <": self.hole_values(
                starting_note=self.lowest_note,
                intervals=(1, 4, 3, 5, 0, 4, 3, 5, 0, 4, 3, 5),
                note_order=music.FLAT_NOTE_ORDER
            ),
            "draw <": self.hole_values(
                starting_note=self.lowest_note,
                intervals=(3, 3, 4, 2, 3, 3, 4, 1, 1, 3, 7, 4),
                note_order=music.FLAT_NOTE_ORDER
            )
        }

    @property
    def lowest_note(self) -> str:
        return f"{self._key.notation}'"

    @property
    def highest_note(self) -> str:
        note = music.MusicExpression(self.lowest_note)
        note.transpose_half_steps(38)
        return note.notation
