import requests
import spotifytools

# -------------------TODO----------------------- #
# > Webapp front-end?
# ---------------------------------------------- #

print("Some sample IDs:")

sample = {
    "B0821LYBJP": "100 BEST 2010S HINDI SONGS"
}

for key, value in sample.items() :
    print (""[:15], f"{key} -", value)

id = input("Playlist ID: ").strip()

print()


headers = {
    'authority': 'eu.web.skill.music.a2z.com', 'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"', 'x-amzn-device-family': 'WebPlayer', 
    'x-amzn-device-time-zone': '+10:00', 
    'x-amzn-timestamp': '1622301069183', 'x-amzn-application-version': '1.0.6458.0', 'x-amzn-device-width': '1920', 
    'x-amzn-device-id': '26026249613099725', # For now, omitting CSRF token and going off of this. Chucks a 500 if this is omitted.
    'x-amzn-page-url': 'https://music.amazon.in/playlists/B07QHJRNZX', 'x-amzn-weblab-id-overrides': '', 'x-amzn-authentication': '{"interface":"ClientAuthenticationInterface.v1_0.ClientTokenElement","accessToken":""}', 'x-amzn-os-version': '1.0', 'x-amzn-session-id': '257-9455010-1764246', 
    'x-amzn-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37', 
    'x-amzn-music-domain': 'music.amazon.in', 'sec-ch-ua-mobile': '?0', 
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37', 
    'x-amzn-device-height': '1080', 'x-amzn-device-language': 'en_IN', 'x-amzn-affiliate-tags': '', 'x-amzn-referer': 'music.amazon.in', 'x-amzn-device-model': 'WEBPLAYER', 'x-amzn-ref-marker': '', 'accept': '*/*', 'origin': 'https://music.amazon.in',  'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://music.amazon.in/', 'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
}

params = (
    ('deeplink', '{"interface":"DeeplinkInterface.v1_0.DeeplinkClientInformation","deeplink":"/playlists/' + id  + '"}'),
)

response = requests.get('https://eu.web.skill.music.a2z.com/api/showHome', headers=headers, params=params)

infile = response.json()
playlistname = infile['methods'][2]['template']['headerText']['text']
playlistby = infile['methods'][2]['template']["headerPrimaryText"]
playlistdesc = infile['methods'][2]['template']["headerSecondaryText"]
items = infile['methods'][2]['template']['widgets'][0]['items']

print(f"{playlistname} - {playlistby}.", playlistdesc)
print('Contains Songs:')

no_songs = 0
song_list = []
for item in items:
    singerfull = item['secondaryText1']
    songname = item["primaryText"]
    songimage = item['image']
    if "," in singerfull:
        i = singerfull.find(",")
        singer = singerfull[0:i]
    elif " &" in singerfull:
        i = singerfull.find(" &")
        singer = singerfull[0:i]
    else:
        singer = str(singerfull)

    song_list.append(f'{singer} - {songname}')
    print(""[:15], song_list[len(song_list)-1])

print(f"{len(song_list)} songs.") 

spdc = input('spdc please: ') 

token, expiry, success = spotifytools.getWebAccessToken(spdc)

if not success:
    print('Maybe check sp_dc cookie?', "You provided:")
    print(spdc)

    while not success:
        spdc = input('spdc please: ')
        token, expiry, success = spotifytools.getWebAccessToken(spdc)

success = None # Reset variable

sp_userid = input("Your userid (generally not the same as display name): ")
sp_playlistname = playlistname
sp_playlistdesc = playlistdesc

if sp_userid == "":
    print('User ID please.')
    while sp_userid == None:
        sp_userid = input("Your userid (generally not the same as display name): ")
if sp_playlistdesc == "":
    sp_playlistdesc = "Sample Description"
if sp_playlistname == "":
    sp_playlistname = f"{sp_userid}'s new playlist"

success, sp_playlistid = spotifytools.createPlaylist(token, sp_userid, sp_playlistname, sp_playlistdesc)
if not success:
    print("Failed to create Playlist.")
else:   
    csv = ""
    for song in song_list:
        success, sp_uri = spotifytools.searchSongs(token, song)
        if success:
            csv += (sp_uri + ",")
        else:
            print(f"Couldn't find song {song} in spotify.")
    if csv != "":
        csv = csv[:-1]
        print(csv)
        spotifytools.addSongsPlaylist(token, sp_playlistid, csv)
    else:
        print("Couldn't resolve any of the songs to spotify.")