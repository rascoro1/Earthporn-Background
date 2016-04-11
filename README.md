# Earthporn-Background
Will change Mac OSX Desktop Background to a picture at reddit.com/r/EarthPorn

This was made to understand API responses.
It will call on mergemypdfs.com:5000/api/reddit/earthporn Flask Restful API.
The response is a list of dictionarys of the Reddit page that contains the top Images.
The Script will install these images.
The Script will choose an image then it will make it your background.

Config File:
  URL='api request'
  DELAY=15 # Minutes between each Background update
  IMG_PATH=/Users/MyName/Pictures # THis is where I will install the pictures from earth porn
  PICTURE_NUM=0 # Dont worry about this it will cycle through the pictures
