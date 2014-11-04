from pulsar import provider
import json

# this read the settings
url_address = provider.ADDON.getSetting('url_address')
icon = provider.ADDON.getAddonInfo('icon') # gets icon
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

# function to validate
def included(value, keys):
    res = False
    for item in keys:
        if item in value:
            res = True 
            break
    return res

def extract_magnets_json(data):
	if not ("No movies found" in data):
		items= json.loads(data) # load the json
		for movie in items['MovieList']:
					resASCII =movie['Quality'].encode('utf-8')
					if included(resASCII, movie_allow) and not included(resASCII, movie_deny):
						name = movie['MovieTitle'] + ' - ' + movie['Size'] + ' - YIFY2 Provider'
						yield {'name' : name,'uri' : movie['TorrentMagnetUrl'], 'info_hash' : movie['TorrentHash'], 'resolution' : values3[resASCII], 'Size' : int(movie['SizeByte'])}

def search(info):
	return []

def search_movie(info):
	provider.notify(message='Searching: ' + info['title'].upper()  + '...', header = None, time = 1500, image = icon)
	url = str(url_address) + "/listimdb.json?imdb_id=" + info['imdb_id']
	response = provider.GET(url)
	return extract_magnets_json(response.data)

def search_episode(info):
	# just movies site
	return []

# This registers your module for use
provider.register(search, search_movie, search_episode)