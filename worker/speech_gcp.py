import json
from google.cloud import speech_v1p1beta1 as speech
from scipy.io import wavfile
import google.oauth2.service_account as service_account

credentials = service_account.Credentials.from_service_account_file(filename='service-credentials.json')
client = speech.SpeechClient(credentials=credentials)

speech_file = "commercial_mono.wav"

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

diarization_config = speech.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=2,
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
for word_info in words_info:
    speaker_tag = word_info.speaker_tag
    if speaker_tag not in speaker_info:
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
    # previous_end_time = end_time
    # print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}, start_time: {word_info.start_time.seconds, start_time_micros}, end_time: {word_info.end_time.seconds, end_time_micros}")
print(speaker_info)
with open("sample_test.json", "w") as outfile:
    json.dump(speaker_info, outfile)

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

rate, data = wavfile.read(speech_file)
print(len(data), rate)
for speaker in speaker_info:
    start_times = speaker_info[speaker]["start_times"]
    end_times = speaker_info[speaker]["end_times"]
    print(start_times, end_times)
    output_prefix = f"speaker{int(speaker)}"
    create_microsecond_chunks(data, rate, output_prefix, start_times, end_times)

    