#!/usr/bin/env python3

from flask import Flask, request, Response, send_file
import jsonpickle
import base64
import io
import logging
import os
import redis
from minio import Minio
import glob
import uuid
import json
import subprocess
import time

# Initialize the Flask application
app = Flask(__name__)
# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# r = redis.from_url(redis_url)
redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379

r = redis.StrictRedis(host=redisHost, port=redisPort, db=0)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
REDIS_KEY = "toDiarization"
VIS_QUEUE = "toVisualize"
# BUCKET_NAME = "working"
INPUT_BUCKETNAME='input'
EMOTION_BUCKETNAME = 'emotion'
OUTPUT_BUCKETNAME = 'output'
VIS_BUCKETNAME = 'visualization'
# ACCESS_KEY = "rootuser"
# SECRET_KEY = "rootpass123"
# MINIO_CLIENT = Minio("localhost:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
print(f"Getting minio connection now for host {minioHost}!")

MINIO_CLIENT = None
try:
    MINIO_CLIENT = Minio(minioHost, access_key=minioUser, secret_key=minioPasswd, secure=False)
except Exception as exp:
    print(f"Exception raised in worker loop: {str(exp)}")


def convert_webm_to_wav(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '1',
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful. WAV file saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Replace 'MgV9c_0.webm' and 'output.wav' with your file paths
# convert_webm_to_wav('MgV9c_0.webm', 'output.wav')


found = MINIO_CLIENT.bucket_exists(INPUT_BUCKETNAME)
if not found:
    MINIO_CLIENT.make_bucket(INPUT_BUCKETNAME)
else:
    print("Bucket already exists")


found = MINIO_CLIENT.bucket_exists(EMOTION_BUCKETNAME)
if not found:
    MINIO_CLIENT.make_bucket(EMOTION_BUCKETNAME)
else:
    print("Bucket already exists")


found = MINIO_CLIENT.bucket_exists(OUTPUT_BUCKETNAME)
if not found:
    MINIO_CLIENT.make_bucket(OUTPUT_BUCKETNAME)
else:
    print("Bucket already exists")


found = MINIO_CLIENT.bucket_exists(VIS_BUCKETNAME)
if not found:
    MINIO_CLIENT.make_bucket(VIS_BUCKETNAME)
else:
    print("Bucket already exists")

@app.route('/upload', methods=['POST'])
def upload():
    # data = request.get_json()
    # file_name = data.get('filename', 'audio')
    # mp3_bytes = base64.b64decode(data.get('mp3', ''))
    
    # # post_data = json.loads(request.data)
    # # mp3_raw = post_data['mp3']
    # # mp3_bytes = base64.b64decode(mp3_raw)
    # mp3_data = io.BytesIO(mp3_bytes)
    # mp3_length = len(mp3_bytes)
    # # file_name = post_data['filename']+".wav"
    post_data = json.loads(request.data)
    mp3_raw = post_data['mp3']
    mp3_bytes = base64.b64decode(mp3_raw)
    with open("temp.webm", "wb") as f:
        f.write(mp3_bytes)
    convert_webm_to_wav("temp.webm", "temp.wav")
    with open("temp.wav", "rb") as f:
        mp3_bytes = f.read()
    os.remove("temp.wav")
    os.remove("temp.webm")
    mp3_data = io.BytesIO(mp3_bytes)
    mp3_length = len(mp3_bytes)
    file_name = post_data['filename']
    
       
    print("Creating filename: ", file_name, mp3_length)
    
    MINIO_CLIENT.put_object(INPUT_BUCKETNAME, 
                  file_name+".wav",  
                  data=mp3_data, 
                  length=mp3_length)
    if ".wav" in file_name:
        file_name = file_name.split('.')[0]
    # file_name =  file_name+'.json'
    # check = {
    #     'file_name': file_name,
    #     'length': mp3_length,
    #     'data': post_data
    # }
    # check_pickled = json.dumps(check).encode('utf-8')
    # MINIO_CLIENT.put_object(INPUT_BUCKETNAME, f'{file_name}', io.BytesIO(check_pickled), len(check_pickled), content_type='application/json')
        

    data = {
        'file_name' : file_name,
    }
    print("Pushing to queue", REDIS_KEY,data)
    count = r.lpush(REDIS_KEY,json.dumps(data))
    r.lpush("logging", f"Pushed file to queue {file_name}")
    print("Current queue length", count)
    response = {
        "hash": file_name, 
        "reason": "Audio enqueued for separation",
        "length": mp3_length
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/queue', methods=['GET'])
def queue():
    current_files = list(map(str,r.lrange(REDIS_KEY, 0, -1)))
    response = {'queue' : current_files}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/list/<bucket>', methods=['GET'])
def list_objects(bucket):
    current_files = MINIO_CLIENT.list_objects(bucket)
    response = {'list' : current_files}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/download/<bucket>/<track>', methods=['GET'])
def download_objects(bucket, track):
    current_files = MINIO_CLIENT.list_objects(bucket)
    obj_data = MINIO_CLIENT.get_object(bucket, track)
    data = obj_data.read()
    print("Len", len(data))
    return send_file(io.BytesIO(data), as_attachment=True, download_name=track, mimetype='audio/wav')    
    #response = {'list' : current_files}
    #response_pickled = jsonpickle.encode(response)
    #return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/track', methods=['GET'])
def get_track():
    args = request.args.to_dict()
    file_id = args['file_id']
    component = args['component'] + ".mp3"
    MINIO_CLIENT.fget_object(file_id, component, component)
    return send_file(component,as_attachment=True)

@app.route('/visualization', methods=['GET'])
def visualize_data():
    # print("Check1")
    # current_files = MINIO_CLIENT.list_objects(VIS_BUCKETNAME)
    # print("Files", current_files)
    # while True:
    #     print("Check2")
    #     message = r.blpop(VIS_QUEUE, timeout=0)
    #     print(message)
    #     if message:
    #         message_data = json.loads(message[1].decode('utf-8'))
    #         filename = message_data["hash"]
    #         response = MINIO_CLIENT.get_object(VIS_BUCKETNAME, filename)
    #         object_content = response.read().decode('utf-8')
    #         vis_data = json.loads(object_content)
    #         print(vis_data)
    #         vis_data["filename"] = filename
    #         response_pickled = jsonpickle.encode(vis_data)
    #         break
    #     else:
    #         time.sleep(1)
    # return Response(response=response_pickled, status=200, mimetype="application/json")
    if r.llen(VIS_QUEUE)>0:
        # vis_data = {
        #     "1":
        #     {
        #         "start_times": [0, 16, 25], 
        #         "end_times": [1, 19, 27], 
        #         "emotion": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0]
        #     },
        #     "2":
        #     {
        #         "start_times": [1, 21], 
        #         "end_times": [16, 24], 
        #         "emotion": [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        #     }
        # }
        # vis_data["filename"] = "check"
        message = r.blpop(VIS_QUEUE, timeout=0)
        message_data = json.loads(message[1].decode('utf-8'))
        filename = message_data["hash"]
        try:
            # Check if the object exists in MinIO
            # MINIO_CLIENT.stat_object(VIS_BUCKETNAME, filename)
            
            # If the object exists, proceed with fetching and processing
            response = MINIO_CLIENT.get_object(VIS_BUCKETNAME, filename)
            object_content = response.read().decode('utf-8')
            vis_data = json.loads(object_content)
            vis_data["filename"] = filename
            response_pickled = jsonpickle.encode(vis_data)
            return Response(response=response_pickled, status=200, mimetype="application/json")

        except Exception as e:
            # Handle the case where the object does not exist
            r.lpush(VIS_QUEUE, message_data)
            error_response = {"error": str(e)}
            response_pickled = jsonpickle.encode(error_response)
            return Response(response=response_pickled, status=404, mimetype="application/json")
        
    else:
        vis_data = {
            "error":"No Visualizations outputs yet"
        }
        response_pickled = jsonpickle.encode(vis_data)
        return Response(response=response_pickled, status=500, mimetype="application/json")


    
        
        

#Health Check endpoint
@app.route('/', methods=['GET'])
def hello():
    return '<h1> Music Separation Server</h1><p> Use a valid endpoint </p>'
# start flask app
app.run(host="0.0.0.0", port=5001)