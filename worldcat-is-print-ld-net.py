import requests
import os
import time
import json
import tqdm
import multiprocessing
import time
import requests
import sys, errno
import json
import os

filename = sys.argv[1]

ip_map = {}



def lookup(line):

	pid = multiprocessing.current_process()._identity[0]
	ip = ip_map[pid]

	
	data = json.loads(line)
	
	if data['is_print'] == True:
		# print(data)

		real_data = None
		for i in data['items']:

			oclc = i['item_link'].split('/')[len(i['item_link'].split('/'))-1].split('&')[0]

			url = 'http://' + ip + ':3000/worldcatld/' + oclc
			try:

				r = requests.get(url, headers={'Connection':'close'})
				if r.text.find(data['isbn']) > -1:
					real_data = r.text 
					break

			except IOError as e:
				print(e)

		# time.sleep(0.25)

		data['match'] = real_data

		# if real_data is not None:
		# 	print(data)
		# 	print(real_data)
		# 	print('--------')

		return json.dumps(data) + '\n'

	else:
		return None

		
	return None


def update_db(add_to_db):
	with open( filename+'.results','a') as f:
		for x in add_to_db:

			f.write(x)


if __name__ == "__main__":

	token = os.environ['do_key']

	# get a list of all active regiions right now
	headers = {"Authorization":"Bearer " + token}

	droplets = requests.get("https://api.digitalocean.com/v2/droplets?tag_name=isbn&per_page=100",headers=headers).json()

	ips =[]
	for x in droplets['droplets']:

		ips.append(x['networks']['v4'][0]['ip_address'])

	

	print("There are ", len(ips), "found")
	for x in range(1,len(ips)+1):
		ip_map[x] = ips[x-1]

	print(ip_map)
	
	results = []

	lock = multiprocessing.Lock()

	with open(filename) as file:

		for result in tqdm.tqdm(multiprocessing.Pool(len(ips)).imap_unordered(lookup, file), total=248060):	


			# print(str(work_counter) + '/' + str(len(oclcs)))

			if result != None:
				results.append(result)

			if len(results) >= 500:
				lock.acquire()
				add_to_db = results
				results = []
				lock.release()

				update_db(add_to_db)

		update_db(results)
			