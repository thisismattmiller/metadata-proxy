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
import sqlite3


ip_map = {}

def lookup(line):

	pid = multiprocessing.current_process()._identity[0]
	ip = ip_map[pid]
	real_data = None


	if line['classify_editions'] is not None:
		data = json.loads(line['classify_editions'])
		

		for e in data:


			url = 'http://' + ip + ':3000/worldcatld/' + e['oclc']
			try:

				r = requests.get(url, headers={'Connection':'close'})
				if r.text.find(line['isbn']) > -1:
					real_data = r.text 
					break

			except IOError as e:
				print(e)

	return json.dumps({"isbn":line['isbn'], "results":real_data})+ '\n'
	
		
	return None


def update_db(add_to_db):
	with open('missing-auth-pub-worldcat.results3','a') as f:
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



	conn = sqlite3.connect('../isbn-lookup/isbn_data.db', timeout=10,check_same_thread=False)
	# conn.row_factory = sqlite3.Row
	conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])

	read_cursor = conn.cursor()
	read_cursor.execute('select * from data where has_classify == 1 and has_worldcat is null and (no_author == 1 or no_publisher == 1);')

	results = []

	lock = multiprocessing.Lock()


	for result in tqdm.tqdm(multiprocessing.Pool(len(ips)).imap_unordered(lookup, read_cursor), total=87464):	


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
		