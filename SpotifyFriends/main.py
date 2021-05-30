from flask import Flask, redirect, url_for, request, make_response
import requests
# from pprint import pprint
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

'''
TODO:
  > Sorting people cards 
    > based on last seen
    > based on alphabetical?
  > Style cookie request page
  > Include instructions on cookie request page
'''

app = Flask(__name__, static_url_path='/static')

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


def getFriendActivity(accessToken):
  #print(f'Recieved access token {accessToken}')
  headers = {
    'Authorization': f'Bearer {accessToken}',
  }

  response = requests.get('https://guc-spclient.spotify.com/presence-view/v1/buddylist', headers=headers).json()
  
  return response

def getWebAccessToken(spdc): 
  headers = {
  }

  cookies = {
      'sp_dc': spdc,
  }

  try:
    response = requests.get('https://open.spotify.com/get_access_token?reason=transport&productType=web_player', headers=headers, cookies=cookies)
    success = True
    if not response:
      print(f'Failed with status {response.status_code}. Maybe check sp_dc cookie? URL changed?')

    responsejson = response.json()

    accessToken = responsejson['accessToken']
    expiry = timeUntilUnixTime(responsejson['accessTokenExpirationTimestampMs'])
  
  except:
    accessToken = "Failed"
    expiry = "Failed"
    success = False

  
  return accessToken, expiry, success

def plural(num):
  if num > 1:
    return "s"
  else:
    return ""

def lastSeen(when):
  #ago = f'{-((when.days * 1440) + (when.hours * 60) + (when.minutes))} minutes'
  if int(when.minutes) + int(when.hours) + int(when.days) == 0:
    s = -when.seconds
    ago = f'Online ({s} second{plural(s)}' + " ago)"

  elif (int(-when.minutes) < 12) and (int(when.hours) + int(when.days) == 0):
    m = -when.minutes
    ago = f'Online ({m} minute{plural(m)}' + " ago)"

  elif int(when.hours) + int(when.days) == 0:
    m = -when.minutes
    ago = f'last seen {m} minute{plural(m)}' + " ago"

  elif int(when.days) == 0:
    h = -when.hours
    ago = f'last seen {h} hour{plural(h)}' + " ago"

  else:
    d = -when.days
    ago = f'last seen {d} day{plural(d)}'  + " ago"

  return ago

@app.route('/')
def home():
  spdc_cookie = request.cookies.get('spdc')
  if spdc_cookie:
    spdc = spdc_cookie
  else:
    return redirect(url_for('getcookie'))

  accessToken, expiry, success = getWebAccessToken(spdc)

  if not success:
    failhtml = '''
      <html>  
      <head>  
          <title>Incorrect Cookie</title>  
          <script>
            function setCookie(cname, cvalue, exdays) {
              var d = new Date();
              d.setTime(d.getTime() + (exdays*24*60*60*1000));
              var expires = "expires="+ d.toUTCString();
              document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
            }
            
            function setspdc() {
              x = new FormData(document.querySelector('form'))
              spdc = x.get('spdc')
              setCookie("spdc", spdc, 365)
              // document.cookie = "spdc=" + spdc + "; expires=";
              alert('Recieved SPDC ' + spdc)
              document.body.innerHTML = '<h1>Saved!</h1><a href="/"><h2>View your friend activity</h2></a>';
            }
          </script>
      </head>  
      <body>  
        <h1>Your cookie seems to be incorrect, or I'm having a bad day. Try checking your cookie?</h1>
        <form method="post" action="javascript:setspdc()">  
            <input type="text" name="spdc" required placeholder="long string of text">
            <input type="submit" value="Submit">
        </form>  
      </body>  
      </html>  
    '''
    return failhtml

  print(f'Access Token: {accessToken},', f'Expires in {expiry.minutes} minutes')
  print()
  friendActivity = getFriendActivity(accessToken)

  # pprint(friendActivity)
  html = """
  <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="/static/w3.css">
      <style>
        .cs240 {
          object-fit: contain; /* Do not scale the image */
          object-position: center; /* Center the image within the element */
          height: 240px;
          width: 240px;
        }
        .mh180 {
          overflow: overlay;
          height: 180px;
        }
        .w280 {
          width: 280px;
        }
        .wrapflow {
          white-space: nowrap;
          overflow-x: hidden;
        }
        .x3434 {
          width:34px; 
          height:34px;
        }
        .w240 {
          width: 240px;
        }

        @media only screen and (max-width: 600px) {
          .w280, .w240 {
            width: 100%;
          }
          .cs240 {
            width: 100%;
          }
        }
      </style>
      <title>
        Friend Activity
      </title>
    </head>
  <body>
      <div class="w3-row-padding">

  
  """

  for friend in friendActivity['friends']:
    ago = lastSeen(timeUntilUnixTime(friend['timestamp']))
    
    user = friend['user']
    username = user['name']
    userlink = user['uri'].replace("spotify:user:", "https://open.spotify.com/user/")
    try:
      userimg = user['imageUrl']
    except:
      userimg = "https://open.scdn.co/cdn/images/icons/Spotify_32.492cdebf.png"

    track = friend['track']
    songname = track['name']
    songlink = track['uri'].replace("spotify:track:", "https://open.spotify.com/track/")
    try:
      songimg = track['imageUrl']
    except:
      songimg = "https://open.scdn.co/cdn/images/icons/Spotify_128.c9ce2f2e.png"

    album = friend['track']['album']
    albumname = album['name']
    albumlink = album['uri'].replace("spotify:album:", "https://open.spotify.com/album/")

    artist = friend['track']['artist']
    artistname = artist['name']
    artistlink = artist['uri'].replace("spotify:artist:", "https://open.spotify.com/artist/")

    where = friend['track']['context']
    playlist = False
    if "playlist" in where['uri']:
      playlist = True
      wherename = where['name']
      whereurl = where['uri'].replace("spotify:playlist:", "https://open.spotify.com/playlist/")

    html += f'''
    <div class="w3-container w3-half w280">
      <div class="w240">
          <h2 class="w3-center wrapflow">
              <img class="userimg w3-circle x3434" src="{userimg}" />

              <a href="{userlink}">
                  {username}
              </a>
          </h2>
          <p class="w3-center username">
              {ago}
          </p>
      </div>
      <div class="w3-card-4 w3-hover-shadow w240">
          <img class="songimg cs240" src="{songimg}" />
          <div class="w3-container w3-center mh180">
              
              <p class="song">
                  Listened to <a href="{songlink}">{songname}</a>.
                  by
                  <a href="{artistlink}">{artistname}</a>
                  in <a href="{albumlink}">{albumname}</a>.
              </p>
              <p class="source">
    '''

    if playlist:
      html += f'''
      Listened through playlist <a href="{whereurl}">{wherename}</a>.
      '''
    elif "album" in where['uri']:
      html += f'''
      Straight from the album <a href="{albumlink}">{albumname}</a>.
      '''
    elif "artist" in where['uri']:
      html += f'''
      Straight from the artist's page <a href="{artistlink}">{artistname}</a>.
      '''

    html += '''
              </p>
            </div>
        </div>
    </div>
    '''

    print(username, ago)

  html += """
  <script>
    setTimeout(function () {
    location.reload();
    }, 15000);
  </script>
  </body></html>
  
  """

  res = make_response(html)
  #res.set_cookie('spdc', spdc)
  
  return res

@app.route('/getcookie', methods = ['GET'])
def getcookie():

  html = '''
  <html>  
  <head>  
      <title>Input Cookie</title>  
      <script>
        function setCookie(cname, cvalue, exdays) {
          var d = new Date();
          d.setTime(d.getTime() + (exdays*24*60*60*1000));
          var expires = "expires="+ d.toUTCString();
          document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
        }

        function setspdc() {
          x = new FormData(document.querySelector('form'))
          spdc = x.get('spdc')
          setCookie("spdc", spdc, 365)
          // document.cookie = "spdc=" + spdc + "; expires=";
          alert('Recieved SPDC ' + spdc)
          document.body.innerHTML = '<h1>Saved!</h1><a href="/"><h2>View your friend activity</h2></a>';
        }
      </script>
  </head>  
  <body>  
      <form method="post" action="javascript:setspdc()">  
          <input type="text" name="spdc" required placeholder="long string of text">
          <input type="submit" value="Submit">
      </form>  
  </body>  
  </html>  
  
  '''
  res = make_response(html)

  return res

app.run('0.0.0.0')