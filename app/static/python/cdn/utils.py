import zlib

from spaces import *

ACCESS_ID = "5POV4IR5H2XWALCF7KWY"
SECRET_KEY = "j7k9MO7SXueLeEbkXdYBAlaZ7XfC1EMdqV3w9KrceHQ"


def compress(filename):
    with open(filename, mode="rb") as fin, open(filename, mode="wb") as fout:
        data = fin.read()
        compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
        print(f"Original size: {sys.getsizeof(data)}")
        # Original size: 1000033
        print(f"Compressed size: {sys.getsizeof(compressed_data)}")
        # Compressed size: 1024

        fout.write(compressed_data)

    with open(filename, mode="rb") as fin:
        data = fin.read()
        compressed_data = zlib.decompress(data)
        print(f"Compressed size: {sys.getsizeof(data)}")
        # Compressed size: 1024
        print(f"Decompressed size: {sys.getsizeof(compressed_data)}")
        # Decompressed size: 1000033


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


def allowed_file(filename):
    return True
