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


dont_want = {'eBook': True,
			 'Musical score': True,
			 'eAudiobook': True,
			 'Audiobook on CD': True,
			 'book_largeprint': True,
			 'Map': True,
			 'Kit': True,
			 'DVD video': True,
			 'Music CD': True,
			 'Book': False,
			 'Music': True,
			 'Audiobook': True,
			 'Braille book': True,
			 'Article': True,
			 'Computer file': True,
			 'Chapter': True,
			 'Website': True,
			 'Bluray Video': True,
			 'Video': True,
			 'Downloadable article': True,
			 'Music LP': True,
			 'Image': True,
			 'Thesis/dissertation': False,
			 'Encyclopedia article': True,
			 'Archival material': True,
			 'Journal, magazine': True,
			 'Continually updated resource': True,
			 'eVideo': True,
			 'Game': True,
			 'Audiobook on Cassette': True,
			 'eMap': True,
			 'eMusic': True,
			 'Downloadable musical score': True,
			 'VHS video': True,
			 'Film': True,
			 'Interactive multimedia': True,
			 'Visual material': True,
			 'Object': True,
			 'Audiobook on LP': True}


def lookup(line):

	pid = multiprocessing.current_process()._identity[0]
	ip = ip_map[pid]

	
	data = json.loads(line)
	
	if data['is_print'] == False:
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

		time.sleep(0.25)

		data['match'] = real_data

		# if real_data is not None:
		# 	print(data)
		# 	print(real_data)
		# 	print('--------')

		return json.dumps(data) + '\n'



	else:
		return line

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
	with open( filename+'.results','a') as f:
		for x in add_to_db:

			f.write(x)


if __name__ == "__main__":

	token = os.environ['do_key']

	# get a list of all active regiions right now
	headers = {"Authorization":"Bearer " + token}

	droplets = requests.get("https://api.digitalocean.com/v2/droplets?tag_name=isbn",headers=headers).json()

	ips =[]
	for x in droplets['droplets']:

		ips.append(x['networks']['v4'][0]['ip_address'])

	

	print("There are ", len(ips), "found")
	for x in range(1,len(ips)+1):
		ip_map[x] = ips[x-1]

	print(ip_map)
	# compelted_oclcs = {}
	# # try to load the .result file first to see if there is anything there
	# if os.path.isfile( filename + '.results'):
	# 	with open( filename+ '.results') as read:
	# 		for l in read:
	# 			d = json.loads(l)
	# 			compelted_oclcs[d['id'].strip()] = True

	# print(len(compelted_oclcs),'already compelted')


	# oclcs = []

	# # remove the completed ones
	# with open(filename) as completed_file:
	# 	for line in completed_file:			
	# 		if line.strip() not in compelted_oclcs:
	# 			oclcs.append(line.strip())

	# ips_use=[]
	# oclcs_work = []
	# for line in oclcs:

	# 	if len(ips_use) == 0:
	# 		ips_use = ips[:]

	# 	ip = ips_use.pop()
		
	# 	data = {'oclc': line.strip(), 'ip':ip, 'data':}
	# 	oclcs_work.append(data)


	# print(len(oclcs_work),' ready to work')

	# work_counter = 0
	results = []

	lock = multiprocessing.Lock()

	with open(filename) as file:

		for result in tqdm.tqdm(multiprocessing.Pool(len(ips)).imap_unordered(lookup, file), total=383687):	


			# print(str(work_counter) + '/' + str(len(oclcs)))

			if result != None:
				results.append(result)

			if len(results) >= 1000:
				lock.acquire()
				add_to_db = results
				results = []
				lock.release()

				update_db(add_to_db)

		update_db(results)
			