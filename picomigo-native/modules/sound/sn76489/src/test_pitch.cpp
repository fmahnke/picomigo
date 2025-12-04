#include "pitch.h"

#include "pico/stdio.h"
#include "pico/stdlib.h"

#include <stdio.h>

#include <iomanip>
#include <iostream>
#include <string>

using std::cout;
using std::endl;
using std::string;

int main() {
    stdio_init_all();

    sleep_ms(2000);

    const string NOTES = "cdefgab";
    const string SHARP_NOTES = "c#d#f#g#a#";

    for (int octave = 0; octave <= 8; ++octave) {
        for (char note : NOTES) {
            string note_name(1, note);
            note_name += std::to_string(octave);
            float frequency = frequency_from_note(note_name);
            cout << std::setw(3) << note_name << ": " << std::fixed
                 << std::setprecision(2) << frequency << " Hz " << endl;

            // Check for sharp notes
            if (SHARP_NOTES.find(note) != string::npos) {
                string sharp_note_name = note_name;
                sharp_note_name.insert(1, "#");
                frequency = frequency_from_note(sharp_note_name);
                cout << std::setw(3) << sharp_note_name << ": " << std::fixed
                     << std::setprecision(2) << frequency << " Hz" << endl;
            }
        }
    }

    return 0;
}
