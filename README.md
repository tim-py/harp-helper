# GUI Application "Harp Helper"
This application provides tuning, transposing and tab notating help aids for Harmonica.

## Dependencies
* Graphics are provided using the PyQT6 cross-platform graphical framework

## Installation
From the top level directory run:
* pip install -e .

## Run
harp-helper

## Music Notation
The music notation used to enter notes is based on the same notation used for
Lilypond:  <letter><accedental><octave>
* letter ("c", "d", "e", "f", "g", "a", or "b")
* accidental (sharp: "is", flat: "es", natural "")
* octave
  * octave 0: ",,," (3 commas)
  * octave 1: ",," (2 commas)
  * octave 2: "," (1 comma)
  * octave 3: "" (omitted)
  * octave 4: "'" (1 apostrophe)
  * octave 5: "''" (2 apostrophes)
  * octave 6: "'''" (3 apostrophes)
  * (etc)

## Apple Silicone Install
* Install Python 3.9 Universal
* Make a copy of Terminal shortcut and name it 'Terminal Rosetta'
* Right click on the copied shortcut, get Info, Check "Open using Rosetta"
* Launch the "Terminal Rosetta" shortcut
* Deactivate any existing virtual environments
  * deactivate
* Create a new virtual environment
  * python3.9 -m venv /path/to/env
* Activate the new environment
  * source /path/to/env/bin/activate
* Install the python requirements
  * pip install -r requirements.txt
* Run the main script
  * python harp_helper/main.py