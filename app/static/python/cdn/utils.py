import os

import requests

# from spaces import Client

ACCESS_ID = "5POV4IR5H2XWALCF7KWY"
SECRET_KEY = "j7k9MO7SXueLeEbkXdYBAlaZ7XfC1EMdqV3w9KrceHQ"


def upload_file(path, filename, bucket_folder):

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


def upload_file_link(url, file_name):
    try:
        r = requests.get(url, allow_redirects=True)
        open(file_name, "wb").write(r.content)
        upload_file(file_name, file_name, "Documents")
        os.remove(file_name)
        return True

    except Exception as e:
        print(e)
        return False


def allowed_file(filename):
    return True
