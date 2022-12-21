import requests, json, os

url = "https://discord.com/api/v10/applications/992107195003043841/role-connections/metadata"

data = [
  {
    "key": 'isstaff',
    "name": 'Staff',
    "description": 'Staff Member of Nebulus',
    "type": 7,
  },
  {
    "key": 'earlysupporter',
    "name": 'Early Supporter',
    "description": 'Joined Nebulus before 12/18/22',
    "type": 7,
  },
  {
    'key': 'courseamount',
    'name': 'Course(s)',
    'description': 'Courses added by the user.',
    'type': 2,
  },
]

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bot {os.environ["BOT_TOKEN"]}',
  }
requests.put(url=url, data=json.dumps(data), headers=headers)