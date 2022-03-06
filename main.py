
import requests
import xmltodict
from xml.dom import minidom

r = requests.get('https://frkqbrydxwdp.compat.objectstorage.eu-frankfurt-1.oraclecloud.com/susr-rpo/')
data = xmltodict.parse(r.content)
items = list(data.items())
print(len(items[0][1]['Contents']))
f = open("text_links.txt", "a")
f1 = open("json_links.txt", "a")
for url in items[0][1]['Contents']:
    if 'txt' in url['Key']:
        f.write(url['Key'])
        f.write('\n')
    else:
        f1.write(url['Key'])
        f1.write('\n')

f.close()
f1.close()
