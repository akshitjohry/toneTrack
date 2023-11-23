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
redis_queue = "toWorker"


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

bucketname='demucs'


def process_message(message):
    try:
        # Parse the message JSON
        message_data = json.loads(message.decode('utf-8'))

        print(message_data)
        # Retrieve song from the message
        filename = message_data["hash"]
        response = client.get_object(bucketname, f'{filename}.wav')
        object_content = response.read()
        print("Check3")
        os.chdir("/lib/TIM-Net_SER/Code/")
        with open(f'{filename}.wav', 'wb') as local_file:
            local_file.write(object_content)
        os.system(f"python3 inference.py --audio_path /lib/TIM-Net_SER/Code/{filename}.wav ")
        print("Check4")
        # for track in ["bass", "drums", "vocals", "other"]:
        #     track_path = f"/data/output/htdemucs/{filename}/{track}.mp3"
        #     with open(track_path, "rb") as track_file:
        #         track_data = track_file.read()
        # client.put_object(bucketname, f'{filename}_{track}.mp3', io.BytesIO(track_data), len(track_data),content_type='audio/mpeg')
        out_filename = f"{filename.split('.')[0]}.json"
        with open(out_filename, "r") as output:
            data = json.load(output)
        json_data = json.dumps(data).encode('utf-8')
        client.put_object(bucketname, f'{filename}_output.json', io.BytesIO(json_data), len(json_data), content_type='application/json')
        # print("Check5")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    while True:
        # Listen for messages in the Redis queue
        print("Check2")
        messages = redis_db.lrange(redis_queue, 0, -1)
        #print(messages)
        message = redis_db.blpop(redis_queue, timeout=0)
        #print(message[1])
        if message:
           process_message(message[1])
        sys.stdout.flush()
        
    
if __name__ == '__main__':
    print("Check")
    main()
