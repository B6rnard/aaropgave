
import requests
import json

response = requests.get('https://api.fbi.gov/wanted/v1/list', params={
 "warning_message" : "SHOULD BE CONSIDERED ARMED AND DANGEROUS"   
})
data = json.loads(response.content)
print(data['total'])
print(data['items'][0-2]['title'])

