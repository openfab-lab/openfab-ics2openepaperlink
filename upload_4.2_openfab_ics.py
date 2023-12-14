#!/usr/bin/env python3

# pip install ics requests Pillow

import sys
import requests
from PIL import Image, ImageDraw, ImageFont
from ics import Calendar
from datetime import date, timedelta

NRDATES = 7
# DEBUG go back X days in the past if ics does not contain enough future events, 0 to disable
DEBUG_PAST_DAYS = 0
mac = "000002CAFCFB483C"   # destination mac address
dither = 0   # set dither to 1 is you're sending photos etc
apip = "192.168.10.169"   # ip address of your access point

dummy = False
if len(sys.argv) > 1 and sys.argv[1] == '-n':
    sys.argv.pop(1)
    dummy = True

dfr = {"Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
       "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"}

today = date.today()
today = today - timedelta(days=DEBUG_PAST_DAYS)

# Calculate the number of days to go back to the last Monday
days_to_last_monday = (today.weekday() - 0) % 7  # 0 represents Monday
# Subtract the calculated days to get the last Monday
last_monday = today - timedelta(days=days_to_last_monday)

# Parse the URL
url = "https://calendar.google.com/calendar/ical/c_fle7ng3r3tkmgat1s95o9bu810%40group.calendar.google.com/public/basic.ics"
cal = Calendar(requests.get(url).text)

next_events = sorted([x for x in cal.events if x.begin.date() >= today])
print(len(next_events))
# if many future events, keep next NRDATES ones
if len(next_events) >= NRDATES:
    next_nrevents = next_events[:NRDATES]
# if not enough events, complete with previous ones up to last Monday
else:
    since_monday_events = sorted([x for x in cal.events if x.begin.date() >= last_monday and x not in next_events])
    next_nrevents = since_monday_events[-(NRDATES - len(next_events)):] + next_events

# Create a new paletted image with indexed colors
image = Image.new('P', (400, 300))

# Define the color palette (white, black, red)
palette = [
    255, 255, 255,  # white
    0, 0, 0,        # black
    255, 0, 0       # red
]

# Assign the color palette to the image
image.putpalette(palette)

# Initialize the drawing context
draw = ImageDraw.Draw(image)

# Define the text lines
lines = []
for x in next_nrevents:
    d = dfr[x.begin.datetime.strftime("%A")]
    db = x.begin.datetime.strftime("%d/%m %H:%M-")
    de = x.end.datetime.strftime("%H:%M")
    lines.append((d, db+de))

# Define the fonts and sizes
# font34 = ImageFont.truetype('fonts/UbuntuMono-Regular.ttf', size=34)
font28b = ImageFont.truetype('fonts/UbuntuMono-Bold.ttf', size=28)
font34b = ImageFont.truetype('fonts/UbuntuMono-Bold.ttf', size=34)


image_logo = Image.open("logo_more.png")
image.paste(image_logo, (36, 5))

voff1 = 67 + 13
voff2 = voff1 + 5
vspace = 30
hoff1 = 4
hoff2 = 151
# Write the text on the image
for i in range(len(lines)):
    draw.text((hoff1, voff1 + i * vspace), lines[i][0], fill=2, font=font34b)  # Use palette index 2 for red color
    draw.text((hoff2, voff2 + i * vspace), lines[i][1], fill=1, font=font28b)  # Use palette index 1 for black color

# Convert the image to 24-bit RGB
rgb_image = image.convert('RGB')

# Save the image as JPEG with maximum quality
image_path = 'output.jpg'
rgb_image.save(image_path, 'JPEG', quality="maximum")

if dummy:
    im = Image.open(image_path)
    f = 4
    im = im.resize((im.width * f, im.height * f), Image.NEAREST)
    im.show()
    exit()

# Prepare the HTTP POST request
url = "http://" + apip + "/imgupload"
payload = {"dither": dither, "mac": mac}  # Additional POST parameter
files = {"file": open(image_path, "rb")}  # File to be uploaded

# Send the HTTP POST request
response = requests.post(url, data=payload, files=files)

# Check the response status
if response.status_code == 200:
    print("Image uploaded successfully!")
else:
    print("Failed to upload the image.")
