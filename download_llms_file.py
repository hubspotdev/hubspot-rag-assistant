import requests

url = "https://developers.hubspot.com/docs/llms-full.txt"
response = requests.get(url)

with open("llms-full.txt", "w") as f:
    f.write(response.text)
