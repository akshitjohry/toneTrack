import os
import json
import redis
import requests

# from flask import Flask, request, Response, send_file, jsonify
import redis
import json
import jsonpickle
import base64
import os
import uuid
import io

# app = Flask(__name__)
REDIS_SERVICE_HOST = os.environ.get('REDIS_SERVICE_HOST') or 'redis'
# REDIS_MASTER_SERVICE_PORT = os.environ.get('REDIS_MASTER_SERVICE_PORT') or 6379
        
redis_db = redis.Redis(host=REDIS_SERVICE_HOST, port=6379)
redis_queue = "toWorker"


from minio import Minio
import os,time,sys

minioHost = os.getenv("MINIO_HOST") or "minio"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
minioAddr = f'{minioHost}:9000'
print(minioAddr)
client = Minio(minioAddr,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

bucketname='my-bucketname'



def process_message(message):
    try:
        # Parse the message JSON
        message_data = json.loads(message.decode('utf-8'))

        # Check if webhook callback is required
        if message_data.get("webhook"):
            payload = message_data.get("payload")
            # Make an HTTP POST request to the webhook
            response = requests.post(message_data["webhook"], json=payload)
            if response.status_code != 200:
                print(f"Webhook request failed with status code: {response.status_code}")
        print(message_data)
        # Retrieve song from the message
        filename = message_data["hash"].decode('utf-8')
        response = client.get_object(bucketname, f'{filename}.mp3')
        object_content = response.read()
        with open(f'{filename}.mp3', 'wb') as local_file:
            local_file.write(object_content)
        os.system(f"python3 -m demucs.separate --out ./ \
                        {filename}.mp3 --mp3")

        for track in ["bass", "drums", "vocals", "other"]:
            track_path = f"{filename}/{track},mp3"
            with open(track_path, "rb") as track_file:
                track_data = track_file.read()
            client.put_object(bucketname, f'{filename}_{track}.mp3', io.BytesIO(track_data), len(track_data),content_type='audio/mpeg')

        # Run DEMUCS separation
        # os.system(f'docker run --rm -i \
        #     -v {mp3_dir}:/data/input \
        #     -v $(pwd)/output:/data/output \
        #     -v $(pwd)/models:/data/models \
        #     xserrat/facebook-demucs:latest \
        #     "python3 -m demucs.separate --out /data/output \
        #     /data/input/{filename}.mp3 --mp3"')

        # Retrieve separated tracks and save to the local file system
        # output_directory = "/tmp/output/mdx_extra_q"
        
        # for track in ["bass", "drums", "vocals", "other"]:
        #     track_path = f"{output_directory}/{filename}/{track}.mp3"
        #     with open(track_path, "rb") as track_file:
        #         # Save to the local file system (you can modify this part based on your needs)
        #         with open(f"/tmp/{track}_{filename}", "wb") as local_track_file:
        #             local_track_file.write(track_file.read())

    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    while True:
        # Listen for messages in the Redis queue
        message = redis_db.blpop(redis_queue, timeout=0)
        print(message[1])
        if message:
            process_message(message[1])

if __name__ == "__main__":
    main()
