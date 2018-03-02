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

	time.sleep(0.25)
	return json.dumps({"isbn":line['isbn'], "results":real_data})+ '\n'
	
	# if data['is_print'] == False:
	# 	# print(data)

	# 	real_data = None
	# 	for i in data['items']:

	# 		oclc = i['item_link'].split('/')[len(i['item_link'].split('/'))-1].split('&')[0]

	# 		url = 'http://' + ip + ':3000/worldcatld/' + oclc
	# 		try:

	# 			r = requests.get(url, headers={'Connection':'close'})
	# 			if r.text.find(data['isbn']) > -1:
	# 				real_data = r.text 
	# 				break

	# 		except IOError as e:
	# 			print(e)

	# 	time.sleep(0.25)

	# 	data['match'] = real_data

	# 	# if real_data is not None:
	# 	# 	print(data)
	# 	# 	print(real_data)
	# 	# 	print('--------')

	# 	return json.dumps(data) + '\n'



	# else:
	# 	return line

	# url = 'http://' + data['ip'] + ':3000/worldcatld/' + data['oclc']


	# try:

	# 	r = requests.get(url, headers={'Connection':'close'})
	# 	time.sleep(0.5)
	# 	if r.text == 'null':
	# 		return None

	# 	return {"id":data['oclc'],"results":r.text}

	# except IOError as e:
	# 	print(e)
	# 	return None
		
	return None


def update_db(add_to_db):
	with open('classify_to_worldcat.results','a') as f:
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
	read_cursor.execute('select isbn, classify_editions from data where has_classify == 1 and has_xisbn == 0 and has_worldcat is null')

	results = []

	lock = multiprocessing.Lock()



	for result in tqdm.tqdm(multiprocessing.Pool(len(ips)).imap_unordered(lookup, read_cursor), total=232199):	


		# print(str(work_counter) + '/' + str(len(oclcs)))

		if result != None:
			results.append(result)

		if len(results) >= 10:
			lock.acquire()
			add_to_db = results
			results = []
			lock.release()

			update_db(add_to_db)

	update_db(results)
		