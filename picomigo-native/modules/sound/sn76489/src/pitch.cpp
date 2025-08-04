#include <cmath>
#include <string>

using std::string;

/// Returns the frequency of a note, in Hz.
///
/// inputs:
///
/// note is a note name and octave
///
/// Example:
///
/// frequency_from_note("a#4");  // returns 466.16

float frequency_from_note(string note) {
    // Define the base frequency for A4
    const float A4_FREQUENCY = 440.0;
    // Define the note names in an octave
    const std::string NOTES = "cdefgab";
    // Define the semitone offsets for each note
    const int SEMITONE_OFFSETS[] = {0, 2, 4, 5, 7, 9, 11};

    // Calculate the semitone offset for the note
    // Extract the note and octave from the input string
    char note_char = note[0];
    int octave = note.back() - '0';
    int semitone_offset = 0;

    if (note_char >= 'a' && note_char <= 'g') {
        semitone_offset = SEMITONE_OFFSETS[NOTES.find(note_char)];
    }

    // Check for sharp or flat
    if (note.length() > 2) {
        if (note[1] == '#') {
            semitone_offset += 1;
        } else if (note[1] == 'b') {
            semitone_offset -= 1;
        }
    }

    // Calculate the semitone difference from A4
    int semitone_difference = semitone_offset + (octave - 4) * 12 - 9;

    // Calculate the frequency

    float base = semitone_difference / 12.0;

    return A4_FREQUENCY * std::pow(2.0, base);
}
