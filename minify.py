# -*- coding: utf-8 -*-
import sys
import requests

try:
    raw_file = sys.argv[1]
except:
    print("Missing input file")
    sys.exit()

# Grab the file contents
with open(raw_file, 'r') as c:
    content = c.read()

# Pack it, ship it
payload = {'input': content}
url = 'https://www.toptal.com/developers/cssminifier/raw'
print("Requesting mini-me of {}. . .".format(c.name))
r = requests.post(url, payload)

# Write out minified version
minified = raw_file.rstrip('.css')+'.min.css'
with open(minified, 'w') as m:
    m.write(r.text)

print("Minification complete. See {}".format(m.name))



