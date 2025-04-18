import requests
import json

response = requests.get('https://api.fbi.gov/wanted/v1/list', params={
    "warning_message": "SHOULD BE CONSIDERED ARMED AND DANGEROUS"
})
data = json.loads(response.content)

print(f"Total results: {data['total']}")

print("\nurls of the first 10 wanted individuals:")
for item in data['items'][:10]:
    print(item['url'])