import redis
import json
import jsonpickle
import base64
import os
import uuid
import io
import sys

REDIS_SERVICE_HOST = os.environ.get('REDIS_SERVICE_HOST') or 'localhost'
# REDIS_MASTER_SERVICE_PORT = os.environ.get('REDIS_MASTER_SERVICE_PORT') or 6379
        
redis_db = redis.StrictRedis(host=REDIS_SERVICE_HOST, port=6379, db=0)
redis_queue = "toDiarization"
redis_queue_emotion = "toEmotion"


from minio import Minio
import os,time,sys

minioHost = os.getenv("MINIO_HOST") or "localhost"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
minioAddr = f'{minioHost}:9000'
print(minioAddr, REDIS_SERVICE_HOST)
client = Minio(minioAddr,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

bucketname='input'
emotion_bucketname = 'emotion'
output_bucketname = 'output'

def process_message(message):
    try:
        # Parse the message JSON
        message_data = json.loads(message.decode('utf-8'))

        print(message_data)
        # Retrieve song from the message
        filename = message_data["file_name"]
        print(filename)
        if ".wav" in filename:
            filename = filename.split('.')[0]
        response = client.get_object(bucketname, f'{filename}.wav')
        object_content = response.read()
        # print("Check3")
        # os.chdir("/lib/TIM-Net_SER/Code/")
        with open(f'{filename}.wav', 'wb') as local_file:
            local_file.write(object_content)
        # filename = "commercial2.wav"
        # os.system(f"python3 speech_diarization.py --speech_file /lib/TIM-Net_SER/Code/{filename}.wav ")
        # os.system(f"python3 speech_diarization.py --speech_file commercial1.wav ")
        # os.system(f"python3 speech_diarization.py --speech_file commercial2.wav --prev_speech_file commercial1.wav --prev_speaker_file commercial1.json ")
        os.system(f"python3 speech_diarization.py --speech_file {filename}.wav ")
        out_filename = f"{filename.split('.')[0]}.json"
        with open(out_filename, "r") as output:
            data = json.load(output)
        json_data = json.dumps(data).encode('utf-8')
        client.put_object(output_bucketname, f'{filename}.json', io.BytesIO(json_data), len(json_data), content_type='application/json')
        vis_data = {
            "data":[]
        }
        json_data = json.dumps(vis_data).encode('utf-8')
        client.put_object(output_bucketname, f'{filename}_vis.json', io.BytesIO(json_data), len(json_data), content_type='application/json')
        # Add all the speaker based chunks to Object Store
        files = sorted(os.listdir('./'))
        prefix = filename.split('.')[0]+"_"
        files = [f for f in files if prefix in f and ".wav" in f]
        for f in files:
            with open(f, "rb") as speaker_file:
                audio_data = speaker_file.read()
            client.put_object(emotion_bucketname, f.split('.')[0]+".wav", io.BytesIO(audio_data), len(audio_data),content_type='audio/mpeg')
            response_data = {
                "hash": f.split('.')[0], 
                "reason": "Song enqueued for separation"
            }
            message_json = json.dumps(response_data)
            redis_db.lpush(redis_queue_emotion, message_json)
        # client.remove_object(bucketname, f'{filename}.wav')
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    while True:
        # Listen for messages in the Redis queue
        # print("Check2")
        messages = redis_db.lrange(redis_queue, 0, -1)
        #print(messages)
        message = redis_db.blpop(redis_queue, timeout=0)
        #print(message[1])
        if message:
           process_message(message[1])
        sys.stdout.flush()
        
    
if __name__ == '__main__':
    # print("Check")
    main()
