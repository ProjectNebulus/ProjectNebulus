from boto3 import session
from botocore.client import Config

ACCESS_ID = 'VCRH4QOPCDEQR5PFNPQM'
SECRET_KEY = 'Vx3pqPbLTGlSvNAhfxPFDto8CskcWOXOjvcW0ziwXys'

# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='sfo3',
                        endpoint_url='https://sfo3.digitaloceanspaces.com',
                        aws_access_key_id=ACCESS_ID,
                        aws_secret_access_key=SECRET_KEY)

# Upload a file to your Space
client.upload_file('cdn.py', 'nebulus-cdn', 'testing.py')
