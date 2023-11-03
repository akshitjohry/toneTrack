import base64
import json
import os

import functions_framework

from cloudevents.http import CloudEvent

from google.cloud import storage

project_id = os.environ.get("GCP_PROJECT")


@functions_framework.cloud_event
def process_image(cloud_event: CloudEvent) -> None:
    """Cloud Function triggered by Cloud Storage when a file is changed.

    Gets the names of the newly created object and its bucket then calls
    detect_text to find text in that image.

    detect_text finishes by sending PubSub messages requesting another service
    then complete processing those texts by translating them and saving the
    translations.
    """

    # Check that the received event is of the expected type, return error if not
    expected_type = "google.cloud.storage.object.v1.finalized"
    received_type = cloud_event["type"]
    if received_type != expected_type:
        raise ValueError(f"Expected {expected_type} but received {received_type}")

    # Extract the bucket and file names of the uploaded image for processing
    data = cloud_event.data
    bucket = data["bucket"]
    filename = data["name"]

    # Process the information in the new image
    detect_text(bucket, filename)

    print(f"File {filename} processed.")
