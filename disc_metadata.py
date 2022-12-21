import requests, json, os, dotenv
dotenv.load_dotenv()

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
  {
    'key': 'date_created',
    'name': 'Joined At',
    'description': 'Date the user joined Nebulus.',
    'type': 5,
  },
  {
    'key': 'schoology_user',
    'name': 'Schoology User',
    'description': 'The user has connected their Schoology account.',
    'type': 7,
  }
]

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bot {os.environ["BOT_TOKEN"]}',
  }
requests.put(url=url, data=json.dumps(data), headers=headers)