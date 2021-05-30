# Convert a playlist from Amazon Music to Spotify
run btfs.py, and give it the playlist ID (/playlist/**_ABCD1234EF_**/). <br>
It'll search the songs through Spotify and add matching ones to a new Spotify Playlist.

Note: btfs.py calls an import of spotifytools.py, and you may need to play with the imports a bit depending on your system.

# What does what
**btfs.py** performs:
* A rip of the playlist provided from Amazon Music
* A parse of the data to obtain Playlist Name, song names, and artists
* A search of the names ripped from the Amazon Playlist on Spotify
* Adding all matched and found songs to a new Playlist on your Spotify Account

**spotifytools.py** contains auxillary functions that:
* Add songs to a Spotify Playlist
* Creates a Spotify Playlist
* Searches for a song in Spotify
* Convert your sp_dc code into an [OAuth Bearer Token](https://www.oauth.com/oauth2-servers/differences-between-oauth-1-2/bearer-tokens/)
