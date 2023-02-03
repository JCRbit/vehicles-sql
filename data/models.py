import json
import requests

url = 'https://parseapi.back4app.com/classes/Car_Model_List?limit=100&keys=Make,Model'
headers = {
    'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',  # This is the fake app's application id
    'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'  # This is the fake app's readonly master key
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))  # Here you have the data that you need

with open(r".\models.json", "w") as f:
    json.dump(data, f, indent=6)
