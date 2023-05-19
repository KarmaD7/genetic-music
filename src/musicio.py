from music21 import *

# 读取MusicXML文件或创建音乐流

FLAT2SHARP = {
    "A-3": "G#3", 
    "A-4": "G#4",
    "A-5": "G#5",
    "A-6": "G#6",
    "B-3": "A#3", 
    "B-4": "A#4",
    "B-5": "A#5",
    "B-6": "A#6",
    "C-3": "B2", 
    "C-4": "B3",
    "C-5": "B4",
    "C-6": "B5",
    "E-3": "D#3", 
    "E-4": "D#4",
    "E-5": "D#5",
    "E-6": "D#6",
}

PITCH2NUM = {
    'rest': 0,
    "C3": 1,
    "C#3": 2,
    "D3": 3,
    "D#3": 4,
    "E3": 5,
    "F3": 6,
    "F#3": 7,
    "G3": 8,
    "G#3": 9,
    "A3": 10,
    "A#3": 11,
    "B3": 12,
    "C4": 13,
    "C#4": 14,
    "D4": 15,
    "D#4": 16,
    "E4": 17,
    "F4": 18,
    "F#4": 19,
    "G4": 20,
    "G#4": 21,
    "A4": 22,
    "A#4": 23,
    "B4": 24,
    "C5": 25,
    "C#5": 26,
    "D5": 27,
    "D#5": 28,
    "E5": 29,
    "F5": 30,
    "F#5": 31,
    "G5": 32,
    "G#5": 33,
    "A5": 34,
    "A#5": 35,
    "B5": 36,
    "C6": 37,
    "C#6": 38,
    "D6": 39,
    "D#6": 40,
    "E6": 41,
    "F6": 42,
    "F#6": 43,
    "G6": 44,
    "G#6": 45,
    "A6": 46,
    "A#6": 47,
    "B6": 48,
    "E7": 53,
}

NUM2PITCH = {v: k for k, v in PITCH2NUM.items()}

def get_music_lists():

    music_list = []
    for i in range(1, 11):
        note_list, length_list, num_list = [], [], []
        # print(i)
        file_path = f'../music/xml/{i}.xml'
        score = converter.parse(file_path)
        # 提取音符并打印
        for note_obj in score.flat:
            # print(note_obj)
            if isinstance(note_obj, note.Note):
                note_list.append(note_obj.nameWithOctave)
                length_list.append(note_obj.duration.quarterLengthNoTuplets)
            elif isinstance(note_obj, note.Rest):
                note_list.append(note_obj.name)
                length_list.append(note_obj.duration.quarterLengthNoTuplets)
        # print(note_list)
        # print(length_list)

        in_tuplets = 0 # todo
        for (note_, length) in zip(note_list, length_list):
            len_in_list = int(length * 4)

            if len_in_list == 0:
                continue
            # print(len_in_list)
            if note_ in FLAT2SHARP:
                note_ = FLAT2SHARP[note_]
            num_list.extend([PITCH2NUM[note_]] * len_in_list)

        # this is uncorrect. to handle.
        if len(num_list) < 128:
            num_list.extend([0] * (128 - len(num_list)))
        else:
            num_list = num_list[:128]

        # print(sum(length_list))
        # print(len(num_list))
        music_list.append(num_list)
        # return num_list
    return music_list

def write_musicxml(num_list: list) -> None:
    music = stream.Stream()
    print("writing musicxml...")
    print(len(num_list))
    for num in num_list:
        # TODO: 0 represents Rest
        n = note.Note(NUM2PITCH[num]) if num != 0 else note.Rest()
        n.duration.quarterLength = 0.25
        music.append(n)
    music.write("musicxml", "genetic_compose.xml")

if __name__ == "__main__":
    music_list = get_music_lists()
    print(music_list)
