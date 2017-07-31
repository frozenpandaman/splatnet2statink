# eli fessler
import requests, json

# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md
url     = 'https://stat.ink/api/v2/battle'
auth    = {'Authorization': 'Bearer emITHTtDtIaCjdtPQ0s78qGWfxzj3JogYZqXhRnoIF4'} # testing account API key
payload = {
	'lobby':  'standard',
	'mode':   'regular',
	'rule':   'nawabari',
	'stage':  'hokke',
	'weapon': 'hokusai',
	'result': 'win',
	'agent':  'splatnet2statink',
	'agent_version': '0.0.1'
}

r = requests.post(url, headers=auth, data=payload)
print r.headers.get('location') # url of uploaded battle