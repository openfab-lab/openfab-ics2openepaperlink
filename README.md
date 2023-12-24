Little script to display next 7 open-door events from our OpenFab public Google calendar ICS on an OpenEpaperLink 4.2" screen


Installing on a RPi:

```
sudo apt install python3.11-venv python3-dev libjpeg9-dev
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

/home/pi/openfab-ics2openepaperlink/upload_4.2_openfab_ics.sh
```
#!/bin/bash

cd /home/pi/openfab-ics2openepaperlink
source venv/bin/activate
python3 upload_4.2_openfab_ics.py
deactivate
```

`crontab -e`
```
*/5 * * * * /home/pi/openfab-ics2openepaperlink/upload_4.2_openfab_ics.sh >> /tmp/epaper_logfile.log 2>&1
```
