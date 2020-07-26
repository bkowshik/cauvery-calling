from pathlib import Path
import datetime

import pytz
import requests
from google.cloud import storage


def upload(path):
    """Upload file to gcs."""

    filename = path.name
    destination_blob_name = 'ksndmc/reservoir-levels/{}'.format(filename)

    bucket_name = 'cauvery-calling-prod'
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(path)
    return '{}/{}'.format(bucket_name, destination_blob_name)


def download_rl_from_ksndmc(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    # Directory with write access to temporarily store the file.
    directory = Path('/tmp')

    now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    filename = '{}.pdf'.format(now.strftime('%Y-%m-%d %H:%M:%S'))

    path = directory / filename

    # URL to download and store on gcs.
    url = 'https://www.ksndmc.org/Uploads/RL.pdf'

    # Download file from url.
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)
    print('Downloaded to: {}'.format(path))

    # Upload file to gcs.
    destination = upload(path)
    print('Uploaded to: {}'.format(destination))

