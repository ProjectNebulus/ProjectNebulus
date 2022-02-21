import requests
email="neel.parpia@gmail.com"
response = requests.get(f"https://www.khanacademy.org/api/internal/user?email={email}")
#print(response.json())

#to do, analyze the data, find 404s that don't work