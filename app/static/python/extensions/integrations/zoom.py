import json
from zoomus import ZoomClient

client = ZoomClient('lLUCahkeRIS_KN8Ilo5hvQ', 'HO1uKHXfEy4mx2ZKOrYy1J8JH2yEMCLj')

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

for user in user_list['users']:
    user_id = user['id']
    print(json.loads(client.meeting.list(user_id=user_id).content))