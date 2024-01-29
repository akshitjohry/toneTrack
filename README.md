# ToneTrack
ToneTrack is a streaming service that allows users to record a conversation through the ToneTrack URL. In real-time, the ToneTrack backend distinguishes different speakers in the conversation, detects the mood of each individual, and provides real-time emotion detection graphs as the conversation is going on.

Use cases:
With virtual meetings being an essential part of almost every industry now, we think ToneTrack is an invaluable asset in several practical applications. Some of them are identified as follows:
* Corporate Online Team meetings: Track employees' emotions over the course of the meeting.
* Therapist Sessions: Deliver valuable insights from client conversations and reshape the treatment
* Online Classes: Assess students' emotions and stress levels.


## Architecture:
![ToneTrack](https://github.com/akshitjohry/toneTrack/blob/main/ToneTrack.png)


## Machine Learning models:
Tonetack at the heart of it, is running two machine learning models. Both of these are deployed as Kubernetes pods and are evoked sequentially using a redis queue between them
* Diarisation Worker
  - Speaker Diarization - Given an audio file, it uses google.cloud.speech.v1p1beta1 APIs to identify the different speakers. This module works independently on each 30s of streamed audio and produces the results.
  - SpeakerIdentification - With the previous Speaker Diarization module, it becomes essential to align speakers from the previous chunk to the current 30s audio chunk. Speaker Identification combines previous chunk to the current chunk and align the speakers in the combined audi and finally present results only for the current chunk
  - Speaker Fragmentation: As toneTrack needs to analyze the emotion for each speaker, the 30s chunk is further divided based on speaker. These fragments are  stored in object store and send to redis queue
  - Additionally this package also post-processes the output from the client which is in a webm format to a wav format which is used for the analysis.
* Emotion Detection:
  - The Machine Learning model for emotion detection is based on the “Temporal Modeling Matters: A Novel Temporal Emotional Modeling for Speech Emotion Recognition”. It uses MFCC features from audio files and uses CNN+LSTM model to identify the emotion. We use the tensorflow package and RAVDESS dataset ( with emotions "angry", "calm", "disgust", "fear", "happy", "neutral","sad","surprise") to train our initial model.
  - Once the emotion for each fragment is obtained, it is integrated with the other fragments' emotion to build a JSON with emotions for the entire 30s audio chunk.


## Demo
[Youtube Link](https://www.youtube.com/watch?v=MzwhJxGk8jE)
