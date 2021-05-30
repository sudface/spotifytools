import requests
from dateutil.relativedelta import relativedelta
from datetime import datetime, timezone

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def addSongsPlaylist(token, pl_id, uris):
    if not "spotify:track:" in uris:
        print("URIS in incorrect format!")
        print(f"Required format: {bcolors.BOLD}{bcolors.FAIL}spotify:track:4cOdK2wGLETKBW3PvgPWqT{bcolors.ENDC}")
        return False # Not suceeded
    
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
    }

    params = (
    ('uris', uris), # Format: 'spotify:track:00QuXoF6LyKwH9xz7lXGdf,spotify:track:6wdyJnmcSeBXUyR6H5gGKd'
    )

    response = requests.post(f'https://api.spotify.com/v1/playlists/{pl_id}/tracks', headers=headers, params=params)

    if response.status_code == 201:
        print(f"Resource successfully created, with Snapshot ID {response.json()['snapshot_id']}")
        return True
    else:
        print(response.json())
        return False

def createPlaylist(token, userid, playlistname, playlistdesc):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    data = '{"name":"' + playlistname + '","description":"' + playlistdesc + '","public":false}'

    response = requests.post(f'https://api.spotify.com/v1/users/{userid}/playlists', headers=headers, data=data)

    rjson = response.json()

    res_type = rjson['type']
    res_name = rjson['name']
    res_link = rjson['external_urls']['spotify']
    res_desc = rjson['description']
    res_id   = rjson['id']

    if response.status_code == 201:
        print(f"New {res_type} created with name {res_name}", "\n", f"Description {res_desc}", "\n", f"Available at {res_link}", "\n", f"ID = {res_id}")
        return True, res_id
    else:
        print(response.json())
        return False, ""

def searchSongs(token, q):
  headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {token}',
  }

  params = (
      ('q', q),
      ('type', 'track'),
      ('limit', '1'),
  )

  response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
  res_json = response.json()
  if res_json['tracks']['items']:
    uri = res_json['tracks']['items'][0]['uri']
    return True, uri
  else:
    return False, ""

def can_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True

def timeUntilUnixTime(epochms):
  
  if can_int(epochms):
    epochms = int(epochms)
  else:
    return datetime.utcnow().replace(tzinfo=timezone.utc)
  
  dateobj = datetime.utcfromtimestamp(epochms/1000).replace(tzinfo=timezone.utc)

  timeUntil = relativedelta(dateobj, datetime.utcnow().replace(tzinfo=timezone.utc))

  return timeUntil

def getWebAccessToken(spdc): 
  headers = {
  }

  cookies = {
      'sp_dc': spdc,
  }

  try:
    response = requests.get('https://open.spotify.com/get_access_token?reason=transport&productType=web_player', headers=headers, cookies=cookies)
    success = True # <--
    if not response:
      print(f'Failed with status {response.status_code}. Maybe check sp_dc cookie? URL changed?')

    responsejson = response.json()

    accessToken = responsejson['accessToken'] # <--
    expiry = timeUntilUnixTime(responsejson['accessTokenExpirationTimestampMs']) # <--
  
  except:
    accessToken = "Failed"
    expiry = "Failed"
    success = False

  return accessToken, expiry, success