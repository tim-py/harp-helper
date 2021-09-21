from harp_helper.harps import Harmonica


class Diatonic10(Harmonica):

    harmonica_type = "d10s"
    harmonica_description = "Diatonic 10 Standard Range"
    keys_available = ("c", "e", "fis", "f", "ees", "d", "des", "b", "bes", "a", "aes", "g")
    action_notation = {
        "blow": "{}",
        "draw": "-{}"
    }

    @property
    def lowest_note(self) -> str:
        return f"{self._key.notation}'"

    @property
    def highest_note(self) -> str:
        return f"{self._key.notation}''''"

    @property
    def tuning_values(self):
        return {
            "blow": self.hole_values(
                starting_note=self.lowest_note,
                intervals=(0, 4, 3, 5, 4, 3, 5, 4, 3, 5)
            ),
            "draw": self.hole_values(
                starting_note=self.lowest_note,
                intervals=(2, 5, 4, 3, 3, 4, 2, 3, 3, 4)
            )
        }
