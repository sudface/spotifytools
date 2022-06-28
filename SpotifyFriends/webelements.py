main_head = """
  <html>
    <head>
      <meta http-equiv="refresh" content="20" >
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

        .sortbox {
          position: fixed; /* Fixed/sticky position */
          top: 20px; /* Place the button at the top of the page */
          right: 30px; /* Place the button 30px from the right */
          z-index: 99; /* Make sure it does not overlap */
          border-radius: 10px; /* Rounded corners */
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
      <div class="w3-dropdown-hover sortbox">
        <button class="w3-button w3-black w3-round-large">Sort?</button>
        <div class="w3-dropdown-content w3-bar-block w3-border" style="right:0">
          <a href="#" class="w3-bar-item w3-button" onclick="setSort(1)">Last Seen (default)</a>
          <a href="#" class="w3-bar-item w3-button" onclick="setSort(2)">Name</a>
        </div>
      </div>

    <div id="cardholder" class="w3-row-padding" style="zoom: 1;">

  
  """
login_head = """
<html>
<head>
	<title>Login to Spotify Friend Activity</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="static/login.css">
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
          document.location.href="/";
        }
      </script>
</head>
<body>
	<div class="limiter">
		<div class="container-login100">
			<div class="wrap-login100 p-b-160 p-t-50">
				<form class="login100-form validate-form" method="post" action="javascript:setspdc()">
					<span class="login100-form-title p-b-43">
"""
login_foot = """
</span>
					
					<div class="wrap-input100 rs1 validate-input" data-validate = "Cookie is required">
						<input class="input100" type="text" name="spdc">
						<span class="label-input100">Long string of text</span>
					</div>
					

					<div class="container-login100-form-btn">
						<input class="login100-form-btn" type="submit" value="Submit">
					</div>
					
					<div class="text-center w-full p-t-23">
						<a href="static/spdc.pdf" class="txt1">
							What's an SP_DC cookie?
						</a>
					</div>
				</form>
			</div>
		</div>
	</div>
</body>
</html>
"""