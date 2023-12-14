import redis
import base64
import os
import io
import json
import uuid

# from pydub import AudioSegment

mp3_dir = "/home/ajay/DSC/lab7-demucs-ajaymopidevi/rest/mp3_storage/"


# Connect to the Redis server
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

# Subscribe to the 'toWorkers' channel
pubsub = redis_db.pubsub()
pubsub.subscribe('toWorkers')

# def separate_and_store(song_data):
#     try:
#         # Generate a unique songhash
#         songhash = str(uuid.uuid4().hex)

#         # Decode and write the MP3 data to a file
#         mp3_binary = base64.b64decode(song_data['mp3'])
#         mp3_filepath = os.path.join(mp3_dir, f"{songhash}.mp3")
#         with open(mp3_filepath, "wb") as mp3_file:
#             mp3_file.write(mp3_binary)

#         # Store the file path in Redis
#         redis_db.set(songhash, mp3_filepath)

#         # Separate the tracks (you need to implement this part)
#         separate_tracks(mp3_filepath, songhash)

#         return {"hash": songhash, "status": "success"}

#     except Exception as e:
#         return {"status": "error", "error": str(e)}

def separate_tracks(mp3_filepath, songhash):
    # Implement track separation logic here
    # You can use a library like Spleeter or your own custom logic
    # Update the function based on your track separation implementation
    pass

# Listen for messages on the 'toWorkers' channel
for message in pubsub.listen():
    print(message)
    if message['type'] == 'message':
        data = json.loads(message['data'])
        # result = separate_and_store(data)
        print(data)
