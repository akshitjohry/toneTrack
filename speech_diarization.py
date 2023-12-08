import json
from google.cloud import speech_v1p1beta1 as speech
from scipy.io import wavfile
import numpy as np
import os
import argparse



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
        enable_word_time_offsets=True,
        use_enhanced = True
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
    speaker = 0
    for word_info in words_info:
        speaker_tag = int(word_info.speaker_tag)
        if speaker_tag not in speaker_info:
            speaker += 1
            speaker_info[speaker_tag] = {
                "start_times": [],
                "end_times": [],
                "words": []
            }
            
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


if __name__ == '__main__':
    # prev_speech_file = None
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--speech_file', type=str, default="")
    parser.add_argument('--prev_speech_file', type=str, default="None")
    parser.add_argument('--prev_speaker_file', type=str, default="None")
    
    args = parser.parse_args()
    
    # prev_speech_file = "prev.wav"
    # previous_info = "prev_SD.json"
    # speech_file = "commercial2.wav"
    prev_speech_file = args.prev_speech_file
    prev_info = args.prev_speaker_file
    speech_file = args.speech_file

    
    
    client = speech.SpeechClient()
    
    if not os.path.exists(prev_speech_file):
        speaker_info = process_file(speech_file)
        out_filename = speech_file.split(',')[0]+'.json'
        with open(out_filename, "w") as outfile:
            json.dump(speaker_info, outfile)

        
    else:
        # Load previous speaker info
        prev_rate, prev_data = wavfile.read(prev_speech_file)
        prev_data = prev_data[int(len(prev_data)*0.75):]
        prev_time = (len(prev_data)/prev_rate)*1000000
        print("Previous time", prev_time)
        f = open(previous_info)
        prev_speaker_info = json.load(f)

        #Load current file
        rate, data = wavfile.read(speech_file)
        data = np.concatenate((prev_data, data))
        print(len(data)/rate)
        
        #Generate new wav file with prev and curr data
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
        

        # Remove overlapping window from the speaker info
        for s in speaker_info:
            start_times = speaker_info[s]["start_times"] 
            end_times = speaker_info[s]["end_times"]
            words = speaker_info[s]["words"]
            speaker_info[s]["start_times"] = []
            speaker_info[s]["end_times"] = []
            for t in range(len(end_times)):
                if end_times[t] > prev_time:
                    start = start_times[t]-prev_time
                    if start < 0:
                        start = 0
                    speaker_info[s]["start_times"].append(start)
                    speaker_info[s]["end_times"].append(end_times[t]-prev_time)
                    speaker_info[s]["words"].append(words[t])
        with open("speaker_SD.json", "w") as outfile:
            json.dump(speaker_info, outfile)
        

    # Divide into chunks based on speaker
    rate, data = wavfile.read(speech_file)
    print(len(data), rate)
    for speaker in speaker_info:
        start_times = speaker_info[speaker]["start_times"]
        end_times = speaker_info[speaker]["end_times"]
        print(start_times, end_times)
        output_prefix = speech_file.split('.')[0] + f"_speaker{int(speaker)}"
        create_microsecond_chunks(data, rate, output_prefix, start_times, end_times)

    # Update curr -> prev
    prev_speaker_info = speaker_info
    prev_speech_file = speech_file
