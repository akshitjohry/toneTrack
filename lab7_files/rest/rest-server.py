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

# Initialize the Flask application
app = Flask(__name__)
# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# r = redis.from_url(redis_url)
redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379

r = redis.StrictRedis(host=redisHost, port=redisPort, db=0)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
REDIS_KEY = "toWorkers"
BUCKET_NAME = "working"
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

@app.route('/upload', methods=['POST'])
def upload():
    post_data = json.loads(request.data)
    mp3_raw = post_data['mp3']
    mp3_bytes = base64.b64decode(mp3_raw)
    mp3_data = io.BytesIO(mp3_bytes)
    mp3_length = len(mp3_bytes)
    file_name = post_data['filename']
    found = MINIO_CLIENT.bucket_exists(BUCKET_NAME)
    if not found:
       MINIO_CLIENT.make_bucket(BUCKET_NAME)
    else:
       print("Bucket already exists")
       
    print("Creating filename: ", file_name)
    MINIO_CLIENT.put_object(BUCKET_NAME, 
                  file_name,  
                  data=mp3_data, 
                  length=mp3_length)

    data = {
        'file_name' : file_name,
    }
    print("Pushing to queue", REDIS_KEY,data)
    count = r.lpush(REDIS_KEY,json.dumps(data))
    r.lpush("logging", f"Pushed file to queue {file_name}")
    print("Current queue length", count)
    response = {
        "hash": file_name, 
        "reason": "Audio enqueued for separation"
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/queue', methods=['GET'])
def queue():
    current_files = list(map(str,r.lrange(REDIS_KEY, 0, -1)))
    response = {'queue' : current_files}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/list', methods=['GET'])
def list_objects():
    current_files = MINIO_CLIENT.list_objects(BUCKET_NAME)
    response = {'list' : current_files}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/track', methods=['GET'])
def get_track():
    args = request.args.to_dict()
    file_id = args['file_id']
    component = args['component'] + ".mp3"
    MINIO_CLIENT.fget_object(file_id, component, component)
    return send_file(component,as_attachment=True)

#Health Check endpoint
@app.route('/', methods=['GET'])
def hello():
    return '<h1> Music Separation Server</h1><p> Use a valid endpoint </p>'
# start flask app
app.run(host="0.0.0.0", port=5001)