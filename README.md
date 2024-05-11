# hikarifield_Product_notification
網頁爬蟲下來通知你的line


mkdir YingRen

cd YingRen

git clone https://github.com/uwing85213/hikarifield_Product_notification.git

cd  hikarifield_Product_notification





python3 -m venv .venv

source .venv/bin/activate



pip3 install requests

pip3 install requests pandas

pip3 install beautifulsoup4

sudo timedatectl set-ntp on

nano autorun.sh

:

#!/bin/bash

source /home/pi/YingRen/hikarifield_Product_notification/.venv/bin/activate

python3 /home/pi/YingRen/hikarifield_Product_notification/Main_Message.py

deactivate

:end


sudo chmod +x autorun.sh

cp autorun.sh /home/pi/autorun.sh

sudo crontab -e

:

0 12 * * * /home/pi/autorun.sh

:end
