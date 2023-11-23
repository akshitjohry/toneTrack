import json
from google.cloud import speech_v1p1beta1 as speech
from scipy.io import wavfile
import numpy as np

client = speech.SpeechClient()
speech_file = "commercial2.wav"


def create_microsecond_chunks(data, rate, output_prefix, start_times, end_times):
    

    for i, (start_time, end_time) in enumerate(zip(start_times, end_times)):
        start_index = int(start_time * rate/1000000)
        end_index = int(end_time * rate/1000000)
        print(start_index, end_index)
        chunk_data = data[start_index:end_index]
        # output_file = f"{output_prefix}_chunk_{i+1}.wav"
        output_file = f"{output_prefix}_start_{start_time}_end_{end_time}.wav"
        wavfile.write(output_file, rate, chunk_data)
        print(f"Chunk {i+1} created: {output_file}")

def process_file(speech_file):
    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=1,
        max_speaker_count=10,
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        diarization_config=diarization_config,
        enable_word_time_offsets=True    
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:

    result = response.results[-1]

    words_info = result.alternatives[0].words

    # Printing out the output:
    speaker_info = {}
    previous_speaker =0
    speaker = 1
    for word_info in words_info:
        speaker_tag = word_info.speaker_tag
        if speaker_tag not in speaker_info:
            speaker_info[speaker] = {
                "start_times": [],
                "end_times": [],
                "words": []
            }
            speaker += 1
        start_time = word_info.start_time.seconds*1000000+word_info.start_time.microseconds
        end_time = word_info.end_time.seconds*1000000+word_info.end_time.microseconds
        
        speaker_info[speaker_tag]["words"].append(word_info.word)  

        if speaker_tag == previous_speaker:
            speaker_info[speaker_tag]["end_times"][-1] = end_time    
        else:
            speaker_info[speaker_tag]["start_times"].append(start_time)
            speaker_info[speaker_tag]["end_times"].append(end_time)
        previous_speaker = speaker_tag
    
    print(speaker_info)
    

    return speaker_info

prev_speech_file = None
prev_speech_file = "commercial1.wav"
previous_info = "commercial1_SD.json"
if prev_speech_file is None:
    speaker_info = process_file(speech_file)
    with open("commercial2_SD.json", "w") as outfile:
        json.dump(speaker_info, outfile)

    prev_speaker_info = speaker_info
else:
    prev_rate, prev_data = wavfile.read(prev_speech_file)
    prev_data = prev_data[int(len(prev_data)*0.75):]
    prev_time = (len(prev_data)/prev_rate)*1000000
    print("Previous time", prev_time)
    f = open(previous_info)
    
    prev_speaker_info = json.load(f)
    rate, data = wavfile.read(prev_speech_file)
    data = np.concatenate((prev_data, data))
    print(len(data)/rate)
    
    wavfile.write("temp.wav", rate, data)
    curr_speaker_info = process_file("temp.wav")
    with open("combined_SD.json", "w") as outfile:
        json.dump(curr_speaker_info, outfile)

    # Align speaker IDs
    speaker_info = {}
    for speaker in curr_speaker_info:
        start_times = curr_speaker_info[speaker]["start_times"]
        found = False
        # prev_start_times = prev_speaker_info[speaker]["start_times"]
        for s in prev_speaker_info:
            prev_start_times = prev_speaker_info[s]["start_times"]
            if prev_start_times[0]==start_times[0]:
                speaker_info[s] = curr_speaker_info[speaker]
                found = True
                break
        if not found:
            speaker_info[speaker] = curr_speaker_info[speaker]
    
    prev_speaker_info = speaker_info

    # Remove overlapping window from the speaker info
    for s in speaker_info:
        start_times = speaker_info[s]["start_times"] 
        end_times = speaker_info[s]["end_times"]
        words = speaker_info[s]["words"]
        speaker_info[s]["start_times"] = []
        speaker_info[s]["end_times"] = []
        for t in range(len(end_times)):
            if end_times[t] > prev_time:
                speaker_info[s]["start_times"].append(start_times[t])
                speaker_info[s]["end_times"].append(end_times[t])
                speaker_info[s]["words"].append(words[t])
    with open("speaker_SD.json", "w") as outfile:
        json.dump(speaker_info, outfile)

# # Divide into chunks based on speaker
# rate, data = wavfile.read(speech_file)
# print(len(data), rate)
# for speaker in speaker_info:
#     start_times = speaker_info[speaker]["start_times"]
#     end_times = speaker_info[speaker]["end_times"]
#     print(start_times, end_times)
#     output_prefix = f"speaker{int(speaker)}"
#     create_microsecond_chunks(data, rate, output_prefix, start_times, end_times)

 