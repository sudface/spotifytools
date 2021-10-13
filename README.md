# spotifytools
An in-progress collection of homemade spotify tools for Python. <br>
Tested on Python 3.8.5 for Linux and 3.9.5 for Windows UWP


# spdc
## What
Spdc is your authentication token. This is quite a hacky project so I won't bother with OAuth. Feel free to pull-request and fix that.

## How
You can get your spdc by logging into spotify online (open.spotify.com) and signing in.
It'll be stored in the cookies for that page

## Where
You can browse your cookies in the Application tab of the Developer Tools in Chromium browsers.
Copy the value of the sp_dc cookie.

![spdc](https://user-images.githubusercontent.com/31204774/120097003-a1814180-c171-11eb-94b8-e7a512d88d17.png)
