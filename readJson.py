import gzip
import json
import requests

baseUrl = 'https://frkqbrydxwdp.compat.objectstorage.eu-frankfurt-1.oraclecloud.com/susr-rpo/'
r = requests.get(baseUrl + 'batch-daily/actual_2022-01-19.json.gz')
data = json.loads(gzip.decompress(r.content))
# for d in data:
#     print(d)
# print(len(data.get('results')))
# print(len(data.get('results')))
# for key in data.get('results')[0].keys():
#     print(key, data.get('results')[0][key])
# print(data.get('results')[0]['legalForms'][0]['value']['code'])
codes = [101, 102, 105, 109, 110, 112]
for item in data.get('results'):
    #     # print(item['legalForms'][0]['value']['code'])
    #     # print(type(item['legalForms'][0]['value']['code']))
    if int(item['legalForms'][0]['value']['code']) in codes:
        print(item)
