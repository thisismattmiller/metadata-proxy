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




def lookup(data):

	url = 'http://' + data['ip'] + ':3000/worldcat/' + data['isbn']


	try:

		r = requests.get(url, headers={'Connection':'close'})
		time.sleep(0.5)
		if r.text == 'null':
			return None

		return {"id":data['isbn'],"results":r.text}

	except IOError as e:
		print(e)
		return None
		



def update_db(add_to_db):
	with open('/Volumes/Byeeee/xisbn/' + filename+'.results','a') as f:
		for x in add_to_db:

			f.write(json.dumps(x) + '\n')


if __name__ == "__main__":

	token = os.environ['do_key']

	# get a list of all active regiions right now
	headers = {"Authorization":"Bearer " + token}

	droplets = requests.get("https://api.digitalocean.com/v2/droplets?tag_name=isbn",headers=headers).json()

	ips =[]
	for x in droplets['droplets']:

		ips.append(x['networks']['v4'][0]['ip_address'])



	compelted_isbns = {}
	# try to load the .result file first to see if there is anything there
	if os.path.isfile('/Volumes/Byeeee/xisbn/' + filename + '.results'):
		with open('/Volumes/Byeeee/xisbn/' + filename+ '.results') as read:
			for l in read:
				d = json.loads(l)
				compelted_isbns[d['id'].strip()] = True

	print(len(compelted_isbns),'already compelted')


	isbns = []

	# remove the completed ones
	with open(filename) as completed_file:
		for line in completed_file:			
			if line.strip() not in compelted_isbns:
				isbns.append(line.strip())

	ips_use=[]
	isbns_work = []
	for line in isbns:

		if len(ips_use) == 0:
			ips_use = ips[:]

		ip = ips_use.pop()
		
		data = {'isbn': line.strip(), 'ip':ip}
		isbns_work.append(data)


	print(len(isbns_work),' ready to work')

	work_counter = 0
	results = []

	lock = multiprocessing.Lock()


	for result in tqdm.tqdm(multiprocessing.Pool(30).imap_unordered(lookup, isbns_work), total=len(isbns_work)):	


		# print(str(work_counter) + '/' + str(len(isbns)))

		if result != None:
			results.append(result)

		if len(results) >= 500:
			lock.acquire()
			add_to_db = results
			results = []
			lock.release()

			update_db(add_to_db)

	update_db(results)
		