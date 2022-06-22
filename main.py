import os
from flask import Flask, request

import sys
from flask import escape
from google.cloud import storage


app = Flask(__name__)


@app.route("/process", methods=['GET'])
def hello_world():
    args = request.args
    image_name = args.get("image", default="Microsoft.png", type=str)
    print(f"Image Name is {image_name}")

    name = os.environ.get("NAME", "World")
    print("Sandy")
    file_cont = download_blob(bucket_name="poc-input-bucket-sandy", source_blob_name=image_name)

    try:
        print("Calling Image API ")
        detect_logos_uri('gs://poc-input-bucket-sandy/' + str(image_name))
    except:
        print("An exception occurred block 2")

    upload_blob_from_memory("poc-output-bucket-sandy", file_cont, image_name + '_processed')
    return "Hello {}!".format(name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


def download_blob(bucket_name, source_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)


    blob = bucket.blob(source_blob_name)

    file_cont = blob.download_as_string()
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, file_cont
        )
    )
    return file_cont
    

def detect_logos_uri(uri):
    """Detects logos in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def upload_blob_from_memory(bucket_name, contents, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
    )

def hello_gcs(event, context):

    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))
    print('Metageneration: {}'.format(event['metageneration']))
    print('Created: {}'.format(event['timeCreated']))
    print('Updated: {}'.format(event['updated']))

