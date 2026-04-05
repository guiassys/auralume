#!/usr/bin/env python3

from music21 import note, stream, chord, scale, meter, tempo
import random
import os


def create_lofi_melody(bpm=70):
    # Stream principal
    melody = stream.Stream()

    # Define escala (base Lo-fi em C maior)
    c_scale = scale.MajorScale('C')
    pitches = [p.nameWithOctave for p in c_scale.getPitches('C3', 'C5')]

    # Escolhe notas aleatórias de início e fim
    start_note = random.choice(pitches)
    end_note = random.choice(pitches)

    start_index = pitches.index(start_note)
    end_index = pitches.index(end_note)

    # Define direção da melodia
    step = 1 if end_index > start_index else -1

    # Geração da melodia
    for i in range(start_index, end_index, step):
        n = note.Note(pitches[i])
        n.quarterLength = 0.5
        melody.append(n)

        r = note.Rest()
        r.quarterLength = 0.5
        melody.append(r)

    # Acorde Lo-fi simples (C major 7 vibe leve)
    lo_fi_chords = [
        chord.Chord(["C4", "E4", "G4"]),
        chord.Chord(["F3", "A3", "C4"]),
        chord.Chord(["G3", "B3", "D4"]),
        chord.Chord(["A3", "C4", "E4"])
    ]

    selected_chord = random.choice(lo_fi_chords)
    selected_chord.quarterLength = 2

    melody.append(selected_chord)

    # Tempo e compasso
    melody.insert(0, tempo.MetronomeMark(number=bpm))
    melody.insert(0, meter.TimeSignature('4/4'))

    # Output
    output_directory = r"C:\devtools\repo\auralith\src\assets\audio\generated"
    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, "lofi_melody.mid")
    melody.write("midi", fp=output_path)

    print(f"MIDI gerado em: {output_path}")


if __name__ == "__main__":
    create_lofi_melody()