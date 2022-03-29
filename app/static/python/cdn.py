# Step 1: Import the all necessary libraries and SDK commands.
import os
import boto3
# Step 2: The new session validates your request and directs it to your Space's specified endpoint using the AWS SDK.
session = boto3.session.Session()
client = session.client('s3',
                        endpoint_url='https://nebulus-cdn.sfo3.digitaloceanspaces.com',
                        # Find your endpoint in the control panel, under Settings. Prepend "https://".
                        region_name='sfo3',  # Use the region in your endpoint.
                        aws_access_key_id='HW5ODS5FRC3ABZUBZMUI',
                        # Access key pair. You can create access key pairs using the control panel or API.
                        aws_secret_access_key="PXVzHLe+Be77KjPzZsWYD4eUyP2HuoSYgrC4/XOnpc8",
                        # Secret access key defined through an environment variable.
                        )
# Step 3: Call the put_object command and specify the file to upload.
client.put_object(
    # Bucket='nebulus-cdn/Images',
    Bucket='nebulus-cdn',
    # The path to the directory you want to upload the object to, starting with your Space name.
    Key='hello-world.txt',  # Object key, referenced whenever you want to access this file later.
    Body=b'Hello, World!',  # The object's contents.
    ACL='public-read',  # Defines Access-control List (ACL) permissions, such as private or public.
    Metadata={  # Defines metadata tags.
        'x-amz-meta-my-key': 'your-value'
    },

)
base = "https://nebulus-cdn.sfo3.digitaloceanspaces.com/"
input = "hello-world.txt"
print(base + input)

# todo: upload/delete file: https://docs.digitalocean.com/products/spaces/resources/s3-sdk-examples/
