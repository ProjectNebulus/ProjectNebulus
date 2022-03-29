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
client.upload_file('/Users/NicholasWang/IdeaProjects/ProjectNebulus/app/static/images/logo.png', 'nebulus-cdn',
                   'logo.png')
base = "https://nebulus-cdn.sfo3.digitaloceanspaces.com/"
input = "nebulus-cdn/logo.png"
print(base + input)

# todo: upload/delete file: https://docs.digitalocean.com/products/spaces/resources/s3-sdk-examples/
