import os

import requests

# from spaces import Client

ACCESS_ID = "VCRH4QOPCDEQR5PFNPQM"
SECRET_KEY = "Vx3pqPbLTGlSvNAhfxPFDto8CskcWOXOjvcW0ziwXys"


def upload_file(path, filename, bucket_folder):
    # Initiate session
    client = Client(
        region_name="sfo3",
        space_name="nebulus-cdn",
        public_key=ACCESS_ID,
        secret_key=SECRET_KEY,
    )

    # Upload a file to your Space
    client.upload_file(
        file=path,
        rename=filename,
        destination=f"{bucket_folder}/",
        extra_args={"ACL": "public-read"},
    )


def upload_file_link(url):
    try:
        name = url.split("/")[-1]
        r = requests.get(url, allow_redirects=True)
        open(name, "wb").write(r.content)
        upload_file(name, name)
        os.remove(name)
        return True

    except Exception as e:
        print(e)
        return False


def allowed_file(filename):
    return True
