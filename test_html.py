import json

line = 89320



with open('worldcat.results') as wc:
	for line_number, l in enumerate(wc, 1):
		

		if line_number == line:
			l = json.loads(l)
			with open('test.html','w') as out:
				l = json.loads(l['results'])

				out.write(l['results'])