from pulsar import provider
import re

# this read the settings
url_address = provider.ADDON.getSetting('url_address')
icon = provider.ADDON.getAddonInfo('icon') # gets icon
name_provider = provider.ADDON.getAddonInfo('name') # gets name
values3 = {'ALL': 0, 'HDTV': 1,'480p': 1,'DVD': 1,'720p': 2 ,'1080p': 3, '3D': 3, "1440p": 4 ,"2K": 5,"4K": 5} #code_resolution steeve

#quality_movie
movie_q1 = provider.ADDON.getSetting('movie_q1') #720p
movie_q2 = provider.ADDON.getSetting('movie_q2') #1080p
movie_q3 = provider.ADDON.getSetting('movie_q3') #3D
movie_allow = []
movie_deny = [] 
movie_allow.append('720p') if movie_q1 == 'true' else movie_deny.append('720p')
movie_allow.append('1080p') if movie_q2 == 'true' else movie_deny.append('1080p')
movie_allow.append('3D') if movie_q3 == 'true' else movie_deny.append('3D')
movie_min_size = float(provider.ADDON.getSetting('movie_min_size'))
movie_max_size = float(provider.ADDON.getSetting('movie_max_size'))
max_size = 10.00 #10 it is not limit
min_size = 0.00

# validate keywords
def included(value, keys):
	value = value.replace('-',' ')
	res = False
	for item in keys:
		if item.upper() in value.upper() and item != '':
			res = True 
			break
	return res

# validate size
def size_clearance(size):
	global max_size
	max_size = 100 if max_size == 10 else max_size
	res = False
	value = float(re.split('\s', size)[0])
	value *= 0.001 if 'M' in size else 1
	if min_size <= value and value <= max_size:
		res = True
	return res

def extract_magnets_json(data):
	if not ("No movies found" in data):
		items = provider.parse_json(data)
		for movie in items['MovieList']:
					resASCII =movie['Quality'].encode('utf-8')
					name = movie['MovieTitle'] + ' - ' + movie['Size'] + ' - ' + name_provider
					if included(resASCII, movie_allow) and not included(resASCII, movie_deny) and size_clearance(movie['Size']):
						yield {'name' : name,'uri' : movie['TorrentMagnetUrl'], 'info_hash' : movie['TorrentHash'], 'resolution' : values3[resASCII], 'Size' : int(movie['SizeByte'])}
					else:
						provider.log.warning(name + '   ***Not Included for keyword filtering or size***')

def search(info):
	return []

def search_movie(info):
	global min_size, max_size
	min_size = movie_min_size
	max_size = movie_max_size
	provider.notify(message='Searching: ' + info['title'].upper()  + '...', header = None, time = 1500, image = icon)
	url = str(url_address) + "/listimdb.json?imdb_id=" + info['imdb_id']
	response = provider.GET(url)
	return extract_magnets_json(response.data)

def search_episode(info):
	# just movies site
	return []

# This registers your module for use
provider.register(search, search_movie, search_episode)