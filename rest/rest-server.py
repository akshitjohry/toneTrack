from flask import Flask, request, Response, send_file, jsonify
import redis
import json
import jsonpickle
import base64
import os
import uuid
import io

app = Flask(__name__)
REDIS_SERVICE_HOST = os.environ.get('REDIS_SERVICE_HOST') or 'localhost'
redis_db = redis.StrictRedis(host=REDIS_SERVICE_HOST, port=6379, db=0)
redis_queue = "toDiarization"


from minio import Minio
import os,time,sys

minioHost = os.getenv("MINIO_HOST") or "localhost"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
# minioHost = "minio"
minioAddr = f'{minioHost}:9000'
print(minioAddr, REDIS_SERVICE_HOST)
client = Minio(minioAddr,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

bucketname='input'
emotion_bucketname = 'emotion'
output_bucketname = 'output'


@app.route('/apiv1/separate', methods=['POST'])
def separate():
    try:
        data = request.json
        mp3_data = data.get('mp3')
        callback_url = data.get('callback').get('url')
        callback_filename = data.get('callback').get('data').get('mp3')
        callback_data = data.get('callback').get('data').get('data')
        # songname = callback_filename.split('/')[1].split('.mp3')[0]
        songhash = str(uuid.uuid4().hex)
        if mp3_data is None:
            response_data = {"error": "No mp3 data provided"}
            status = 400
        else:
            mp3_binary = base64.b64decode(mp3_data)
            ioBuffer = io.BytesIO(mp3_binary)
            #mp3_filepath = os.path.join(mp3_dir, f"{songhash}.mp3")
            # with open(mp3_filepath, "wb") as mp3_file:
            #     mp3_file.write(ioBuffer.getvalue())
            mp3_filepath = f"{songhash}.wav"
            client.put_object(
                bucketname,
                mp3_filepath,
                io.BytesIO(mp3_binary),
                len(mp3_binary),
                content_type='audio/mpeg'
            )
            # redis_db.set(songhash, f'{songhash}.mp3')
            # redis_db.publish('toWorkers', json.dumps({songhash: mp3_filepath}))
            # redis_db.rpush("filepaths", mp3_filepath)
            # Return the response
            response_data = {
                "hash": songhash, 
                "reason": "Song enqueued for separation"
            }
            message_json = json.dumps(response_data)
            redis_db.lpush(redis_queue, message_json)
            
            status = 200
    except Exception as e:
        response_data = {
            "hash": "unknown",
            "error": str(e)
        }
        status = 500
    response_pickled = jsonpickle.encode(response_data)
        
    return Response(response=response_pickled, status= status, mimetype="application/json")
    
    
@app.route('/apiv1/queue', methods=['GET'])
def get_queue():
    try:
        # filepaths = redis_db.lrange("filepaths", 0, -1)
        # filepaths = redis_db.keys('*')
        # queue_data = []
        # for f in filepaths:
        #     songhash = os.path.splitext(os.path.basename(f.decode()))[0]
        #     queue_data.append({
        #         "hash": songhash
        #     })
        messages = redis_db.lrange(redis_queue, 0, -1)

        queue_data = [json.loads(message.decode('utf-8'))["hash"] for message in messages]

        response_data = {
            'queue': queue_data 
        }
        status = 200
    
    except Exception as e:
        response_data = {
            'queue': [],
            'error': str(e)
        }
        status = 500
    response_pickled = jsonpickle.encode(response_data)
        
    return Response(response=response_pickled, status = status, mimetype="application/json")
    

@app.route('/apiv1/track/<songhash>/<track_type>', methods=['GET'])
def get_track(songhash, track_type):
    try:
        # Validate the track type
        valid_track_types = ['bass', 'vocals', 'drums', 'other']
        if track_type not in valid_track_types:
            raise ValueError(f"Invalid track type: {track_type}")
        try:
            obj_data = client.get_object(bucketname, f'{songhash}_{track_type}.mp3')
            data = obj_data.read()
            print("Len", len(data))
            return send_file(io.BytesIO(data), as_attachment=True, download_name=f"{songhash}_{track_type}.mp3", mimetype='audio/mpeg')
        except Exception as e:
            return jsonify({"message": str(e)}), 410
    except ValueError as ve:
        return jsonify({"message": str(e)}), 400
    except FileNotFoundError as fe:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    return jsonify({"message": f"{track_type} for {songhash} downloaded successfully"}), 200
    
@app.route('/apiv1/remove/<songhash>/track', methods=['DELETE'])
def remove_track(songhash):
    try:
        filename = f'{songhash}.mp3'
        client.remove_object(bucketname, filename)
        valid_track_types = ['bass', 'vocals', 'drums', 'other']
        for track in valid_track_types:
            filename = f'{songhash}_{track}.mp3'
            print(filename)
            client.remove_object(bucketname, filename)
        
        return jsonify({"message": f"Track for {songhash} removed successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500    
    return jsonify({"message": f"Track for {songhash} removed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
