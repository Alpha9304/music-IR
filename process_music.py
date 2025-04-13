import sys
import partitura as pt

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

    #print("Compute Note Array of Part with Some information:") #format is (...default info, note ID, pitch spelling letter, accidental (0 = flat, 1 = sharp?), octave num, ''(if grace nots), key sig num 1 (accidentals), key sig num 2 (mode), time_sig num, time_sig denom, beats)
    #use this, lots of info and better formed than straight time sign estimate...
    #for part in parts:
    #    print(pt.musicanalysis.compute_note_array(part, include_pitch_spelling = True, include_key_signature = True))#, include_time_signature = True, include_grace_notes = True))

def extract_features(score):
    parts = score.parts

    #get number of parts
    num_parts = len(parts)

    #get tempo

    key_counts = {}
    #get most frequent/main key signature
    for part in parts:
        note_array = print(pt.musicanalysis.compute_note_array(part, include_key_signature = True))
        for note in note_array:
            key_sig_accidentals = note[9]
            key_sig_mode = note[10] #how to translate this to a numeric identifier?; can't just sum them...

    #get number of key_changes/key signatures

    #get number of time signatures

    #get instrument names or maybe just num instruments?

    #get dynamics

    #get number of rests 
    num_rests = 0
    for part in parts:
        rests = part.rests
        num_rests += rests

    #get average number of measures per part
    total_measures = 0
    for part in parts:
        measures = part.measures
        total_measures += len(measures)

    avg_measures = total_measures/num_parts

    

def main(): #take this away later so this file can just be run by the system
    input_filename = sys.argv[1]
    input_score = pt.load_score(input_filename) #this means the UI will have to take in the uploaded file and put it in the system to load it; and then delete it after
    test_out_library(input_score)
    #print(parts)
    #print(input_score_parts.key_signature_map(input_score_parts.notes[0].start.ts))
    #

if __name__ == '__main__':
    main()