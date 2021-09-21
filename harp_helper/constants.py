NAME = "Harp Helper"
APP_NAME = "harp-helper"
VERSION = "0.0.1"
FULL_RELEASE_NAME = f"{NAME} v{VERSION}"

NOTATION_HELP = """<H1>Music Notation Help</H1>

<H2>Entering Note Values</H2>
Entering music expressions (either in the input box or from a file) can be done using the same LaTex syntax
as Lilypond&trade;. It's made up of only 3 parts (note values are not used for this application):
<ul>
<li>The note letter (c, d, e, f, g, a ,b)
<li>The note accidental ("es" for flat, "is" for sharp, omit for natrual)
<li>The octave.  (commas, apostrophes, or blank)
    <ul>
    <li>,, references the lowest octave on a piano: c1 - b1</li>
    <li>, references the second octave on the piano: c2 - b2</li>
    <li>(omitted) references the third octave on the piano: c3 - b3</li>
    <li>' references the fourth octave on the piano: c4 (middle C) to b4</li>
    <li>'' references the fifth octave on the piano: c5 - b5
    <li><i>and so on...</i> 
    </ul> 
</ul> 

<H2>Examples</H2>
<ul>
<li> Middle C: c'
<li> F sharp above middle C: fis'
<li> A flat in the lowest space on the bass clef: aes,
<li> G above the top line of the treble clef: g''
</ul>

<H2>Putting Notes Together</H2>
Chords are not supported by this application, but melodies are expressed using this notation.
Each note is place one after another separated by a space.  For example, the melody to
"Mary Had A Little Lamb" would start of like this:
<blockquote cite="https://www.singing-bell.com/mary-had-a-little-lamb/">
b' a' g' a' b' b' b' a' a' a' b' d'' d''
b' a' g' a' b' b' b' b' a' a' b' a' g'
</blockquote>
"""