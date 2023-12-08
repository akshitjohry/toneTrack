#!/usr/bin/env python3

from minio import Minio
import os,time,sys

minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"

client = Minio(minioHost,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

# bucketname='demucs'
files_to_add=["minio-config.yaml"]

while True:
    bucketnames = ['input', 'emotion', 'output']
    for bucket in bucketnames:    
        if not client.bucket_exists(bucket):
            print(f"Create bucket {bucket}")
            client.make_bucket(bucket)

    buckets = client.list_buckets()
    print(buckets)
    for bucket in buckets:
        print(f"Bucket {bucket.name}, created {bucket.creation_date}")
            
    #     print(f"Objects in {bucket} are originally:")
    #     for thing in client.list_objects(bucket, recursive=True):
    #         print(thing.object_name)
            
    #     try:
    #         for filename in files_to_add:
    #             print(f"Add file {filename} as object {filename}")
    #             client.fput_object(bucket, filename, f"./{filename}")
    #     except ResponseError as err:
    #         print("Error when adding files the first time")
    #         print(err)

        print(f"Objects in {bucket.name} are now:")
        for thing in client.list_objects(bucket.name, recursive=True):
            print(thing.object_name)
            # client.remove_object(bucket.name, thing.object_name)

    sys.stdout.flush()
    time.sleep(10)