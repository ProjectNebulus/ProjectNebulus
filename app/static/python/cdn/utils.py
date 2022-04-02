from boto3 import session
from botocore.client import Config
import requests
import os

ACCESS_ID = "VCRH4QOPCDEQR5PFNPQM"
SECRET_KEY = "Vx3pqPbLTGlSvNAhfxPFDto8CskcWOXOjvcW0ziwXys"


def upload_file(file_name, path):
    # Initiate session
    cdn_session = session.Session()
    client = cdn_session.client(
        "s3",
        region_name="sfo3",
        endpoint_url="https://sfo3.digitaloceanspaces.com",
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=SECRET_KEY,
    )

    # Upload a file to your Space
    client.upload_file(path, "nebulus-cdn", file_name, ExtraArgs={"ACL": "public-read"})


def upload_file_link(url):
    try:
        name = url.split("/")[-1]
        r = requests.get(url, allow_redirects=True)
        open(name, "wb").write(r.content)
        upload_file(name, name)
        os.remove(name)
        return True
    except:
        return False


def allowed_file(filename):
    return True
