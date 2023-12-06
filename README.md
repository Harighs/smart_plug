# Electromizer

### Overview

Welcome to Electromizer, an innovative project designed to revolutionize home electronics automation
based on electricity prices. At the heart of this initiative is the goal to optimize power usage
by seamlessly adapting to fluctuating electric prices. When prices are low, Electromizer ensures
your system operates at full capacity, maximizing efficiency. Conversely, during periods of high
prices, the system intelligently minimizes usage, providing both cost savings and environmental
benefits.

### Initial setup

The following are the process involved for initial setup

1. Clone this repository
2. Navigate to the clone directory `cd smart_plug`
3. Install all necessary python packages
4. Execute the following command to start the API_SERVICES
   `python3 api_services.py`
5. You will see the API_SERVICES running of the following link
   `http://192.168.1.166:8080/api/`
6. Using the above services you can perform all the Raspberry Pi operations
   For example: Accessing the GPIO pins, activating and deactivating relays and more.

### Contact
# Project Owner
Mag.Dr. Peter Sommerer, Vienna, Austria

# Developers

Harishankar Govindsamy | harishankarghs@gmail.com
Muthukumar Neelamegam | kumar.neelamegam17@gmail.com


## Scripts

######################
  # This service is used to download the data from awattar and smartmeter
  GNU nano 5.4  
# /etc/systemd/system/smart_plug.service

[Unit]
Description=Smart Plug Service is Running - download master data

[Service]
ExecStart=/usr/bin/python3 /home/pi/smart_plug/main_services/masterdata_services.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target


######################
# This service is used to communicate with the api and pi 
  GNU nano 5.4    
# /etc/systemd/system/smart_plug_data_download.service

[Unit]
Description=Smart Plug Service is Running

[Service]
ExecStart=/usr/bin/python3 /home/pi/smart_plug/main_services/api_services.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target


######################
  GNU nano 5.4                                                                               
# /etc/systemd/system/smart_plug_data_download.service

[Unit]
Description=Smart Plug - Auto mode - Service is Running

[Service]
ExecStart=/usr/bin/python3 /home/pi/smart_plug/main_services/auto_mode.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target


######################

Commands
# sudo nano /etc/systemd/system/smart_plug_data_download.service                                                                
# sudo nano /etc/systemd/system/smart_plug.service                                                                                                                                       

sudo systemctl start smart_plug_data_download.service
sudo systemctl start smart_plug.service
sudo systemctl start smart_plug_auto_mode.service

sudo systemctl stop smart_plug_data_download.service
sudo systemctl stop smart_plug.service
sudo systemctl stop smart_plug_auto_mode.service


sudo systemctl status smart_plug_data_download.service
sudo systemctl status smart_plug.service
sudo systemctl status smart_plug_auto_mode.service


sudo systemctl restart smart_plug_data_download.service
sudo systemctl restart smart_plug.service
sudo systemctl restart smart_plug_auto_mode.service


watch -n 1 sudo systemctl status smart_plug.service
journalctl -xe | grep smart_plug_auto_mode.service

pi@raspberrypi:~/smart_plug $ sudo nano /etc/systemd/system/smart_plug_data_download.service
pi@raspberrypi:~/smart_plug $ sudo nano /etc/systemd/system/smart_plug_auto_mode.service
pi@raspberrypi:~/smart_plug $ sudo nano /etc/systemd/system/smart_plug.service
######################


crontab -e


# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command

# This task restarts the "Auto mode" service every 30 minutes
*/30 * * * * sudo service smart_plug_auto_mode restart && echo "Service smart_plug_auto_mode restarted at $(date)" >> /var/log/smart_plug_auto_mode-restart.log


# This task restarts the "Master data download" service every 28 hours
0 */28 * * * sudo service smart_plug_data_download restart  && echo "Service smart_plug_data_download restarted at $(date)" >> /var/log/smart_plug_data_download-restart.l>


# This task restarts the "API" service every 48 hours
0 0 */2 * * sudo service smart_plug restart && echo "Service smart_plug restarted at $(date)" >> /var/log/smart_plug-restart.log


# Testing the service to restart every minute 
# * * * * * sudo service smart_plug restart


######################
  GNU nano 5.4                                         /tmp/crontab.4BC13D/crontab *                                                 
# This task restarts the "Auto mode" service every 30 minutes
*/30 * * * * sudo systemctl restart smart_plug_auto_mode

# This task restarts the "Master data download" service every 28 hours
0 */28 * * * sudo systemctl restart smart_plug_data_download

# This task restarts the "API" service every 48 hours
0 0 */2 * * sudo systemctl restart smart_plug


# Testing the service to restart every minute
# * * * * * sudo service smart_plug restart



######################
 /etc/systemd/system/smart_plug_auto_mode.timer  
 [Unit]
Description=Run smart_plug_auto_mode every 5 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target



######################
sudo systemctl status smart_plug_auto_mode.timer



######################




##########################################################################################################################
########################################################################################################################


NEW SCRIPTS:
03.11.23


######################

  GNU nano 5.4                                                    /etc/systemd/system/smart_plug.timer                                                             
[Unit]
Description=Run smart_plug every 48 hours

[Timer]
OnBootSec=48h
OnUnitActiveSec=48h

[Install]
WantedBy=timers.target

######################


  GNU nano 5.4                                             /etc/systemd/system/smart_plug_data_download.timer *                                                    
[Unit]
Description=Run smart_plug_data_download every 12 hours

[Timer]
OnBootSec=12h
OnUnitActiveSec=12h

[Install]
WantedBy=timers.target



######################

  GNU nano 5.4                                               /etc/systemd/system/smart_plug_auto_mode.timer                                                        
[Unit]
Description=Run smart_plug_auto_mode every 30 minutes

[Timer]
OnBootSec=30min
OnUnitActiveSec=30min

[Install]
WantedBy=timers.target

##########################################################################################################################
########################################################################################################################

  GNU nano 5.4                                            /etc/systemd/system/smart_plug_data_download.service *                                                   
# /etc/systemd/system/smart_plug.service

[Unit]
Description=Smart Plug Service - To Download Awattar and Smart-meter data

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/smart_plug/main_services/masterdata_services.py
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target

######################

  GNU nano 5.4                                              /etc/systemd/system/smart_plug_auto_mode.service                                                       
# /etc/systemd/system/smart_plug_auto_mode.service

[Unit]
Description=Smart Plug - Auto mode

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/smart_plug/main_services/auto_mode.py
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target


######################

  GNU nano 5.4                                                   /etc/systemd/system/smart_plug.service                                                            
# /etc/systemd/system/smart_plug.service

[Unit]
Description=Smart Plug - API Service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/smart_plug/main_services/api_services.py
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target

##########################################################################################################################

# 06.12.2023
# Restart all the Electromizer Services
0 3 * * * sudo systemctl restart smart_plug_data_download.service

3 3 * * * sudo systemctl restart smart_plug_auto_mode.service

5 3 * * * sudo systemctl restart smart_plug.service

##########################################################################################################################


