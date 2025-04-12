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

def create_feature_vector(score): #note in midis some of this data may be missing and will default to something; how do we indicate this?
    parts = score.parts #a part meaning instrument
    print("Initial Key Signatures of Parts:")
    for part in parts:
        print(part.key_signature_map(part.notes[0].start.t)) #returns [number of sharps/flats(+#/-#), mode (major = 1, minor = 0?)]
    
    print("Estimated key signatures of Parts:") #I think this is more accurate thaan key signature and it accounts for not having the key; will have to convert to numbers for the array
    for part in parts:
        print(pt.musicanalysis.estimate_key(part))

    '''
    print("Estimated tempo, meter, and beat information of Parts:") #weird output
    for part in parts:
        print(pt.musicanalysis.estimate_time(part))
    '''

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

    print("Time estimates of Parts:") #weird output for some parts; maybe get key)sig from note array directly? or skip parts, only need first one
    for part in parts:
        print(pt.musicanalysis.estimate_time(part.note_array()))



def main(): #take this away later so this file can just be run by the system
    input_filename = sys.argv[1]
    input_score = pt.load_score(input_filename) #this means the UI will have to take in the uploaded file and put it in the system to load it; and then delete it after
    create_feature_vector(input_score)
    #print(parts)
    #print(input_score_parts.key_signature_map(input_score_parts.notes[0].start.ts))
    #

if __name__ == '__main__':
    main()