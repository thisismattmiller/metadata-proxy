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
import glob


filename = sys.argv[1]

ip_map = {}
error_count = {}


def lookup(oclc_id):

	pid = multiprocessing.current_process()._identity[0]
	ip = ip_map[pid]

	
	# print(oclc_id)


	url = 'http://' + ip + ':3000/worldcatld/' + oclc_id
	try:

		r = requests.get(url, headers={'Connection':'close'})
		time.sleep(0.1)

		if "Error report" in r.text:
			# print("error:",ip,oclc_id)
			error_count[ip]+=1
			return None

		else:
			json.dump({"oclc":oclc_id,"results":r.text },open('/Volumes/Byeeee/worldcat-data/'+oclc_id,'w'))

	except IOError as e:
		print(e)
		return None


	return oclc_id
	


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
		error_count[ips[x-1]] = 0

	print(ip_map)
	
	results = []

	lock = multiprocessing.Lock()


	print("Checking existing files")

	completed_oclcs = {}
	for oclc_file in glob.iglob('/Volumes/Byeeee/worldcat-data/*'):
		completed_oclcs[os.path.basename(oclc_file)] = True


	work = []

	to_work = json.load(open(filename))

	for l in to_work:
		if l not in completed_oclcs:
			work.append(l)
		# else:
		# 	print("skipping",l)

	counter = 0

	#len(ips)
	for result in tqdm.tqdm(multiprocessing.Pool(len(ips)).imap_unordered(lookup, work), total=len(work)):	

		if result is not None:
			counter+=1
			if counter % 10000 == 0:
				print(result)


		pass
