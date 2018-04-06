import requests
import os
import time

token = os.environ['do_key']

# get a list of all active regiions right now
headers = {"Authorization":"Bearer " + token}

droplets = requests.get("https://api.digitalocean.com/v2/droplets?tag_name=isbn&per_page=100",headers=headers).json()

for d in droplets['droplets']:
  r = requests.delete("https://api.digitalocean.com/v2/droplets/"+str(d['id']),headers=headers)
  print(r.status_code)
