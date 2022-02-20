import requests
profile="nicholaswang0503"
response = requests.get(f"https://www.khanacademy.org/api/internal/user/streak?username={profile}")
print(response.text)

#to do, analyze the data, find 404s that don't work