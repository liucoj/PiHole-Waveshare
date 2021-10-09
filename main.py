#!/usr/bin/python
import os
import json
import urllib.request as urllib2
import logging
from waveshare_epd import epd2in13b_V3
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import time
import traceback

logging.basicConfig(level=logging.DEBUG)

# Set current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# get api data
try:
  f = urllib2.urlopen('http://localhost/admin/api.php')
  json_string = f.read()
  parsed_json = json.loads(json_string)
  adsblocked = parsed_json['ads_blocked_today']
  ratioblocked = parsed_json['ads_percentage_today']
  status = parsed_json['status']
  f.close()



# Init Screen
  epd = epd2in13b_V3.EPD()
  logging.info("init and Clear")
  epd.init()
  epd.Clear()
  time.sleep(1)
  
  # Load graphic
  logging.info("Drawing")
  fontF = ImageFont.truetype(FredokaOne, 32)
  fontP = ImageFont.truetype(FredokaOne, 20)
  HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
  HRYimage = Image.new('1', (epd.height, epd.width), 255)
  drawry = ImageDraw.Draw(HRYimage)
  draw = ImageDraw.Draw(HBlackimage)
  # img = Image.open("./logoA.jpg")
  # HRYimage.paste(img, (150,20))
  draw.text((20,20), str(adsblocked), font = fontF, fill = 0)
  draw.text((20,50), str("%.1f" % round(ratioblocked,2)) + "%", font = fontF, fill = 0)
  draw.text((120,60), str(status), font = fontP, fill = 0)
  draw.text((120,30), '[ h0Le ]', font = fontP, fill = 0)

  # epd.display(epd.getbuffer(img), epd.getbuffer(HBlackimage))
  epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13b_V3.epdconfig.module_exit()
    exit()