import sys
import partitura as pt
import re
import numpy as np
from collections import OrderedDict
import statistics as stats
import os
import warnings
from numpy.linalg import norm
import json

#convert (accidentals, mode) to a unique single digit; major is 1, minor is -1...
key_sig_map = {(0, -1): 0, (0, 1): 1, (1, -1): 2, (1, 1): 3, (-1, -1): 4, (-1, 1): 5, (2, -1): 6, (2, 1): 7, (-2, -1): 8, (-2, 1): 9, (3, -1): 10, (3, 1): 11, (-3, -1): 12, (-3, 1): 13, 
               (4, -1): 14, (4, 1): 15, (-4, -1): 16, (-4, 1): 17, (5, -1): 18, (5, 1): 19, (-5, -1): 20, (-5, 1): 21, (6, -1): 22, (6, 1): 23, (-6, -1): 24, (-6, 1): 25, (7, -1): 26, 
               (7, 1): 27, (-7, -1): 28, (-7, 1): 29}

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


def compute_instrument_cats(instrument_list):
    categories = []
    for instrument in instrument_list:
        for key in instrument_categories:
            for instr in instrument_categories[key]:
                if(instr in instrument): #instr in categorized list is most simple (no numberings, tec.)
                    categories.append(key)
    return categories



def read_info(file):
    '''
    Reads information.txt
    '''
    collection = {}
    with open(file) as f:
        for line in f:
            line_arr = line.strip().split("!!!")
            for i in range(len(line_arr)):
                line_arr[i] = line_arr[i].strip()
            midi_file_name = line_arr[0]
            collection[midi_file_name] = line_arr

    return collection

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
    
    print("Estimated Tempo:")
    for part in parts:
        tempo = pt.musicanalysis.estimate_time(part)["tempo"]
        print(tempo)
        break

#vector similarity computation (cosine)
def cosine_sim(x, y):
    length = len(y)
    if(len(x) < len(y)):
        length = len(x)
    num = np.dot(x[:length], y[:length])
    if num == 0:
        return 0
    return num / (norm(x) * norm(y))


def extract_features(input_filename):
    input_score = pt.load_score(input_filename) 
    parts = input_score.parts
    performed_music = pt.load_performance(input_filename) #ignores key signature information
    performed_parts = performed_music.performedparts
    
    #get velocities from the performance
    onset_velocity_per_part = OrderedDict()
    for part in performed_parts:
        #print(part.note_array().dtype)
        note_array = part.note_array()
        for note in note_array:
            #print(note)
            #get velocity dict for part; onset to keep the arrays aligned
            if(note[0] not in onset_velocity_per_part):
                onset_velocity_per_part[note[0]] = [note[5]]
            else:
                onset_velocity_per_part[note[0]].append(note[5])


    #get number of parts
    num_parts = len(parts)
    #print("number of instruments", num_parts)

    #get tempo

    key_counts = {}
    time_sig_counts = {}
    parts_list = []
    tempo = -1 #each part should have the same tempo
    #get most frequent/main key signature
    for part in parts:
        if(tempo == -1):
            tempo = pt.musicanalysis.estimate_time(part)["tempo"]

        note_array = pt.musicanalysis.compute_note_array(part, include_key_signature = True, include_time_signature = True)
        for note in note_array:
            #key signature information
            key_sig_accidentals = note[9]
            key_sig_mode = note[10] 
            key_sig_code = key_sig_map[(key_sig_accidentals, key_sig_mode)]
            if key_sig_code in key_counts:
                key_counts[key_sig_code] += 1
            else:
                key_counts[key_sig_code] = 1

            #time signature information
            time_sig_num = note[11]
            time_sig_denom = note[12]
            if (note[11], note[12]) in time_sig_counts:
                time_sig_counts[(note[11], note[12]) ] += 1
            else:
                time_sig_counts[(note[11], note[12]) ] = 1

      
            

        #collect part names
        parts_list.append(part.part_name)


    #these key stats are not not necesssary, inherent to the key section of the vector...
    most_frequent_key = max(key_counts, key=key_counts.get)
    #print("most frequent key code:", most_frequent_key)

    #get number of key_changes/key signatures
    num_key_signatures = len(key_counts)
    #print("num key signatures: ", num_key_signatures)



    #get number of time signatures
    #print(time_sig_counts)
    num_time_signatures = len(time_sig_counts)
    #print("num time signatures", num_time_signatures)

    #get main (most frequent) time signature
    most_frequent_time_signature = max(time_sig_counts, key = time_sig_counts.get)
    #print("most frequent time signature:", most_frequent_time_signature)

    #get num instruments
    num_instruments = len(parts_list)
    #print("Number of Instruments:", num_instruments)

    #get instrument categories codes
    instr_categories = compute_instrument_cats(parts_list)
    #print("Categories codes: ", instr_categories)
    
    #print("Instrument list: ", parts_list)

    #get dynamic variety; this is often missing. use velocity instead

    #get note velocity over all parts by averaging total over parts
    all_part_velocity = []
    for onset in onset_velocity_per_part:
        total_velocity = np.divide(np.sum(np.array(onset_velocity_per_part[onset])), num_parts)
        all_part_velocity.append(total_velocity)


    #get dynamic variety: sample max, min, mean, and mode, median from this array
    max_velocity = max(all_part_velocity)
    #print("Max Velocity:", max_velocity)

    min_velocity = min(all_part_velocity)
    #print("Min Velocity:", min_velocity)

    mean_velocity = stats.mean(all_part_velocity)
    #print("Mean Velocity: ", mean_velocity)

    med_velocity = stats.median(all_part_velocity)
    #print("Median Velocity: ", med_velocity)

    mode_velocity = stats.mode(all_part_velocity)
    #print("Mode Velocity: ", mode_velocity )

    #get number of rests 
    num_rests = 0
    for part in parts:
        rests = part.rests
        num_rests += len(rests)
    #print("total rests: " , num_rests)

    #get average number of measures per part
    total_measures = 0
    for part in parts:
        measures = part.measures
        total_measures += len(measures)

    avg_measures = total_measures/num_parts
    #print("avg measures per  part: ", avg_measures)


    #constuct the feature vector
    feature_vector = [0] * 59

    #key information, one slot per key (0-29)
    for key in key_counts:
        feature_vector[key] = key_counts[key] #encodes the number and variety of signatures, as well as the most and least frequent one

    #time signature information: main signature num, denom, and number of time signatures (30-32)
    feature_vector[30] = int(most_frequent_time_signature[0])
    feature_vector[31] = int(most_frequent_time_signature[1])
    feature_vector[32] = num_time_signatures

    #instrument information: number of instruments and which categories are present (0 or 1); note category 0 is other; slots (33-50)
    feature_vector[33] = num_instruments 
    for i in range(len(instr_categories)):
        #print(instr_categories[i])
        feature_vector[33 + instr_categories[i]] = 1 
    
    if(len(instr_categories) == 0): #non of the defined categories of instruments were present
        feature_vector[50] = 1

    #velocity (total of all parts!) information: max, min, mean, median, and mode (slots 51-55)
    feature_vector[51] = int(max_velocity)
    feature_vector[52] = int(min_velocity)
    feature_vector[53] = float(mean_velocity)
    feature_vector[54] = int(med_velocity)
    feature_vector[55] = int(mode_velocity)

    #rest information: number of rests (slot 56)
    feature_vector[56] = num_rests 

    #measure information: length aka average per part (slot 57)
    feature_vector[57] = avg_measures 

    #tempo information (slot 58)
    feature_vector[58] = float(tempo)

    return feature_vector #should be python dtypes not np dtypes

def vectorize_collection(save=False):
    path = "./midi-collection"
    midi_file_names = os.listdir(path)
    vector_col = {}
    for i in range(len(midi_file_names)):
        name = midi_file_names[i]
        #print(name) #line that helps see what file has issues
        vector = extract_features("./midi-collection/" + name)
        vector_col[name] = vector

    if(save):
        with open("vector_collection.json", "w") as f:
            json.dump(vector_col, f)

    return vector_col

def compute_most_similar(query_vec, collection_vecs, weight_vec, k=5):
    #print("query vector:", query_vec)
    midi_score_list = []
    top_k = []
    for key in collection_vecs:
        vector = collection_vecs[key]
        weighted_vector = [vector[i] * weight_vec[i] for i in range(len(vector))]
        weighted_q_vector = [query_vec[i] * weight_vec[i] for i in range(len(vector))]
        score = cosine_sim(weighted_q_vector, weighted_vector)
        midi_score_list.append((key, float(score), vector)) #vector for now, just to look at it

    midi_score_list.sort(key = lambda x: x[1], reverse=True)
    #print(midi_score_list)

    for i in range(k):
        top_k.append(midi_score_list[i])
    return top_k




def main(): 
     
    warnings.filterwarnings("ignore") #partitura gives a lot of warnings, may just be old...
    input_filename = sys.argv[1]
    use_precomputed = sys.argv[2] #TEST/CONSTRUCTION ONLY, COMMENT THIS OUT DURING REAL USE; will always use precomputed for real use

    midi_col_info = read_info('information.txt')
    #print(midi_col_info)

    #input_score = pt.load_score(input_filename)
    #test_out_library(input_score)

    input_vector = extract_features(input_filename)
    #print("Input vector", input_vector)

    if(use_precomputed != "true"):
        print("Vectorizing...")
        midi_vecs = vectorize_collection(True)
    else:
        with open('vector_collection.json') as json_f:
            midi_vecs = json.load(json_f)

    
    #print(midi_vecs)
    
    weight_vector = [1] * 59
    for i in range(30):
        weight_vector[i] *= 1.5 #weight key counts higher bc they are more important; I think this helped 
    
    weight_vector[33] *= 0.8 #I think num instruments is less important, so *0.8

    for i in range(34, 51):
        weight_vector[i] *= 1.5 #multiplier bc instrument type more important

    weight_vector[56] **= 2 #blow up larger numbers to emphasize rests (empty space); didn't do much, maybe just db size issue?

    weight_vector[57] *= 0.75 #times 0.75 because I think length of song is less important

    weight_vector[58] *= 2 #I think tempo should be considered a bit more

    top_k_similar = compute_most_similar(input_vector, midi_vecs, weight_vector)
    top_k_info = []
    for i in range(len(top_k_similar)):
        midi_file = top_k_similar[i][0]
        song_name = midi_col_info[midi_file][3]
        composer = midi_col_info[midi_file][1]
        top_k_info.append([song_name, composer])
    
    
    print(json.dumps(top_k_info)) #the php will take all prints as output, use json to give it dtypes other than string


    #might want to weight instruments higher, maybe?...want to capture space more..weight num rests? like maybe squared to blow up larger numbers
    #weights so far haven't changed anything, db too small? also next, try weight instruments and key higher; prob with Ida Red...really cared about tempo which is good but...

    #do pre-vectorization next...once the database is bigger/finalized, use it to save time(took like 7 minutes!)...; would need to write line by line the vectors...
    #also consider tweaking the prepared vectors for testing speed...
if __name__ == '__main__':
    main()