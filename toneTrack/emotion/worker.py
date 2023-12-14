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
redis_queue = "toEmotion"


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
vis_bucketname = 'visualization'

redis_vis_queue = "toVisualize"

def process_message(message):
    try:
        # Parse the message JSON
        message_data = json.loads(message.decode('utf-8'))

        print(message_data)
        # Retrieve song from the message
        filename = message_data["hash"]
        response = client.get_object(emotion_bucketname, f'{filename}.wav')
        object_content = response.read()
        # print("Check3")
        os.chdir("/lib/TIM-Net_SER/Code/")
        with open(f'{filename}.wav', 'wb') as local_file:
            local_file.write(object_content)
        os.system(f"python3 inference.py --audio_path /lib/TIM-Net_SER/Code/{filename}.wav ")
        
        out_filename = f"{filename.split('.')[0]}.json"
        with open(out_filename, "r") as output:
            data = json.load(output)
        
        json_data = json.dumps(data).encode('utf-8')
        client.put_object(output_bucketname, f'{filename}_output.json', io.BytesIO(json_data), len(json_data), content_type='application/json')
        
        #TODO: Check the filenames
        # temp = filename.split('start_')
        # start_time = int(temp[1].split('_end_')[0])
        # end_time = int(temp[1].split('_end_')[1].split('_speaker')[0])
        # speaker_id = int(temp[1].split('_end_')[1].split('_speaker')[1].split('.')[0])
        # vis_file = temp[0]+"vis.json"
        # print("Visualization file", vis_file)
        # response = client.get_object(output_bucketname, vis_file)
        # object_content = response.read().decode('utf-8')
        # json_data = json.loads(object_content)
        # print(json_data)
        # vis_data = {
        #     "start":start_time,
        #     "end":end_time,
        #     "speaker":speaker_id,
        #     "emotion":data['emotion'],
        # }
        # json_data['data'].append(vis_data)
        # print(json_data)        
        # json_data = json.dumps(json_data).encode('utf-8')
        # client.put_object(output_bucketname, vis_file, io.BytesIO(json_data), len(json_data), content_type='application/json')
        temp = filename.split('start_')
        start_time = int(temp[1].split('_end_')[0])
        end_time = int(temp[1].split('_end_')[1].split('_speaker')[0])
        
        is_last = False
        if "last" in filename:
            is_last = True
            speaker_id = str(int(temp[1].split('_end_')[1].split('_speaker')[1].split('_')[0]))
        else:
            speaker_id = str(int(temp[1].split('_end_')[1].split('_speaker')[1].split('.')[0]))
        vis_file = temp[0].split('_')[0]+".json"
        print("Visualization file", vis_file, start_time, end_time)
        
        response = client.get_object(output_bucketname, vis_file)
        object_content = response.read().decode('utf-8')
        json_data = json.loads(object_content)
        print(json_data)
        json_data[speaker_id]["emotion"][start_time:end_time] = [data['pred'] for i in range(start_time, end_time)]
        print(json_data)        
        json_data = json.dumps(json_data).encode('utf-8')
        client.put_object(output_bucketname, vis_file, io.BytesIO(json_data), len(json_data), content_type='application/json')
        if is_last:
            # vis_file = vis_file.split('_')[0]+'.json'
            response_data = {
                "hash": vis_file, 
                "reason": "Song enqueued for separation"
            }
            message_json = json.dumps(response_data)
            redis_db.lpush(redis_vis_queue, message_json)
            print("Vis Queue", response_data)
            client.put_object(vis_bucketname, vis_file, io.BytesIO(json_data), len(json_data), content_type='application/json')

        # client.remove_object(emotion_bucketname, f'{filename}.wav')
        # print("Check5")
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
