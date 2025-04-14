import sys
import partitura as pt
import re

#convert (accidentals, mode) to a unique single digit
key_sig_map = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3, (-1, 0): 4, (-1, 1): 5, (2, 0): 6, (2, 1): 7, (-2, 0): 8, (-2, 1): 9, (3, 0): 10, (3, 1): 11, (-3, 0): 12, (-3, 1): 13, 
               (4, 0): 14, (4, 1): 15, (-4, 0): 16, (-4, 1): 17, (5, 0): 18, (5, 1): 19, (-5, 0): 20, (-5, 1): 21, (6, 0): 22, (6, 1): 23, (-6, 0): 24, (-6, 1): 25, (7, 0): 26, 
               (7, 1): 27, (-7, 0): 28, (-7, 1): 29}

instrument_categories = {1: ["Acoustic Grand", "Bright Acoustic", "Electric Grand", "Honky-Tonk", "Electric Piano", "Harpsichord", "Clavinet"], #Piano
                         2: ["Celesta", "Glockenspiel", "Music Box", "Vibraphone", "Marimba", "Xylophone", "Tubular Bells", "Dulcimer"], #Chromatic Percussion
                         3: ["Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ", "Reed Organ", "Accoridan", "Harmonica", "Tango Accordian"], #Organ
                         4: ["Nylon String Guitar", "Steel String Guitar", "Electric Jazz Guitar", "Electric Clean Guitar", "Electric Muted Guitar", #Guitar
                                    "Overdriven Guitar", "Distortion Guitar", "Guitar Harmonics"],
                         5: ["Acoustic Bass", "Electric Bass", "Fretless Bass", "Slap Bass", "Synth Bass"], #Bass
                         6: ["Violin", "Viola", "Cello", "Contrabass", "Tremolo Strings", "Pizzicato Strings", "Orchestral Strings", "Timpani"], #Solo Strings
                         7: ["String Ensemble", "SynthStrings", "Choir Aahs", "Voice Oohs", "Synth Voice", "Orchestra Hit"], #Ensemble
                         8: ["Trumpet", "Trombone", "Tuba", "Muted Trumpet", "French Horn", "Brass Section", "SynthBrass"], #Brass
                         9: ["Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe", "English Horn", "Bassoon", "Clarinet"], #Reed
                         10: ["Piccolo", "Flute", "Recorder", "Pan Flute", "Blown Bottle", "Shakuhachi", "Whistle", "Ocarina"], #Pipe
                         11: ["Square Wave", "Saw Wave", "Syn. Calliope", "Chiffer Lead", "Charang", "Solo Vox", "5th Saw Wave", "Bass & Lead"], #Synth Lead
                         12: ["Fantasia", "Warm Pad", "Polysynth", "Space Voice", "Bowed Glass", "Metal Pad", "Halo Pad", "Sweep Pad"], #Synth Pad
                         13: ["Ice Rain", "Soundtrack", "Crystal", "Atmosphere", "Brightness", "Goblin", "Echo Drops", "Star Theme"], #Synth Effects
                         14: ["Sitar", "Banjo", "Shamisen", "Koto", "Kalimba", "Bagpipe", "Fiddle", "Shanai"], #Ethnic
                         15: ["Tinkle Bell", "Agogo", "Steel Drums", "Woodblock", "Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal"], #Percussive
                         16: ["Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet", "Telephone Ring", "Helicopter", "Applause", "Gunshot"] #Sound effects
}


def compute_instrument_cats_code(instrument_list):
    categories = []
    for instrument in instrument_list:
        for key in instrument_categories:
            for instr in instrument_categories[key]:
                if(instr in instrument): #instr in categorized list is most simple (no numberings, tec.)
                    categories.append(key)
    return hash(categories)



def read_data(file):
    '''
    Reads the data
    '''
    documents = []
    labels = []
    with open(file) as f:
        for line in f:
            line_arr = line.strip().split()
            label = line_arr[1]
            document = ' '.join(line_arr[3:len(line_arr) - 1])
            documents.append(document)
            labels.append(label)

def test_out_library(score): #note in midis some of this data may be missing and will default to something; how do we indicate this

    parts = score.parts #a part meaning instrument
    print("Initial Key Signatures of Parts:")
    for part in parts:
        print(part.key_signature_map(part.notes[0].start.t)) #returns [number of sharps/flats(+#/-#), mode (major = 1, minor = 0?)]
    
    print("Estimated key signatures of Parts:") #I think this is more accurate thaan key signature and it accounts for not having the key; will have to convert to numbers for the array
    for part in parts:
        print(pt.musicanalysis.estimate_key(part))


    '''
    print("Tempo Direction of Parts:") #empty...
    for part in parts:
        print(part.tempo_directions)

    print("Dynamics of Parts:") #empty
    for part in parts:
        print(part.dynamics)
    '''

    '''
    print("Time estimates of Parts:") #weird output
    for part in parts:
        print(pt.musicanalysis.estimate_time(part))
    '''

    '''
    print("Time estimates of Parts:") #(beat, offset output is too much info); also sometimes estimates ar decimal
    for part in parts:
        print(pt.musicanalysis.estimate_time(part.note_array()))
        break
    '''

    print("Names of Parts:")
    for part in parts: #encode names somehow. sometimes it gives kind of generic names like midi out #2
        print(part.part_name)

    '''
    print("Time estimates of Parts Getting Numerator and Denom:") #weird output for some parts; maybe get key)sig from note array directly? or skip parts, only need first one; ometimes voice is bad..
    for part in parts:
        notes = part.note_array()
        time_info = pt.musicanalysis.estimate_time(notes)
        numerator = time_info.get("meter_numerator")
        denominator = time_info.get("meter_denominator")
        print(str(numerator) + "/" + str(denominator))
    '''

    print("Get Part Key Signatures:") #some scores may not have... and it doesn't match estimate, which is more correct
    for part in parts:
        key_sigs = part.key_sigs
        for key in key_sigs:
            print(key.name)

    print("Get Part Time Signatures:") #this worked! seems to be common info
    for part in parts:
        time_sigs = part.time_sigs
        for time in time_sigs:
            print(str(time.beats) + "/" + str(time.beat_type))

    print("Get Part Dynamics:") #empty sometims but we have enough feaatures...
    for part in parts:
        dynamics = part.dynamics
        for dyna in dynamics:
            print(dyna)

    print("Get Part Tempo Directions:")
    for part in parts:
        tempo_dirs = part.tempo_directions
        for dir in tempo_dirs:
            print(dir)

    print("Get Num Rests Per Part:")
    for part in parts:
        rests = part.rests
        print(len(rests))

    print("Get Num Measures Per Part:")
    for part in parts:
        measures = part.measures
        print(len(measures))

    print("Compute Note Array of Part with Some information:") #format is (...default info, note ID, pitch spelling letter, accidental (0 = flat, 1 = sharp?), octave num, ''(if grace nots), key sig num 1 (accidentals), key sig num 2 (mode), time_sig num, time_sig denom, beats)
    #use this, lots of info and better formed than straight time sign estimate...
    #for part in parts:
    #    print(pt.musicanalysis.compute_note_array(part, include_pitch_spelling = True, include_key_signature = True))#, include_time_signature = True, include_grace_notes = True))

def extract_features(score):
    parts = score.parts

    #get number of parts
    num_parts = len(parts)
    print("number of instruments", num_parts)

    #get tempo

    key_counts = {}
    time_sig_counts = {}
    parts_list = []
    #get most frequent/main key signature
    for part in parts:
        note_array = pt.musicanalysis.compute_note_array(part, include_key_signature = True, include_time_signature = True)
        for note in note_array:
            #key signature information
            key_sig_accidentals = note[9]
            key_sig_mode = note[10] #how to translate this to a numeric identifier?; can't just sum them...
            key_sig_code = key_sig_map[(key_sig_accidentals, key_sig_mode)]
            if key_sig_code in key_counts:
                key_counts[key_sig_code] += 1
            else:
                key_counts[key_sig_code] = 1

            #time signature information
            time_sig_num = note[11]
            time_sig_denom = note[12]
            time_sig_code = hash((note[11], note[12]))
            if time_sig_code in time_sig_counts:
                time_sig_counts[time_sig_code] += 1
            else:
                time_sig_counts[time_sig_code] = 1

        #collect part names
        parts_list.append(part.name)

    most_frequent_key = max(key_counts, key=key_counts.get)
    print("most frequent key code:", most_frequent_key)

    #get number of key_changes/key signatures
    num_key_signatures = len(key_counts)
    print("num key signatures: ", num_key_signatures)

    #get number of time signatures
    print(time_sig_counts)
    num_time_signatures = len(time_sig_counts)
    print("num time signatures", num_time_signatures)

    #get num instruments
    num_instruments = len(parts_list)
    print("Number of Instruments:", num_instruments)

    #get instrument categories code
    cats_code = compute_instrument_cats_code(parts_list)
    print("Categories code: ", cats_code)
    
    print("Instrument list: ", parts_list)

    #get dynamic variety; this is often missing. maybe use velocity from pretty midi?

    #get dynamic loudness

    #get number of rests 
    num_rests = 0
    for part in parts:
        rests = part.rests
        num_rests += len(rests)
    print("total rests: " , num_rests)

    #get average number of measures per part
    total_measures = 0
    for part in parts:
        measures = part.measures
        total_measures += len(measures)

    avg_measures = total_measures/num_parts
    print("avg measures per  part: ", avg_measures)

    

def main(): #take this away later so this file can just be run by the system
    input_filename = sys.argv[1]
    input_score = pt.load_score(input_filename) #this means the UI will have to take in the uploaded file and put it in the system to load it; and then delete it after
    test_out_library(input_score)
    #extract_features(input_score)
    #print(parts)
    #print(input_score_parts.key_signature_map(input_score_parts.notes[0].start.ts))
    #

if __name__ == '__main__':
    main()