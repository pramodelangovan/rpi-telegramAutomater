# rpi-telegramAutomater
Basic framework to build on telegram bot to automate

1. To start clone this repo
2. Install dependencies:
    sudo pip3 install telepot==12.7
    sudo pip3 install picamera==1.13
    sudo pip3 install rpi-backlight==2.1.0
3. Rename constants.sample.py to constants.py
4. Edit the constants.py to add 
    
    
    a. ownerChatId : Telegram User ID
    b. botApi : Telegram bot Api key
    c. systemName : name of your bot/machine
    d. allowedChatId : add other telegram user id's to allow to send commands to telegram bot, (default : [ownerChatId])
    
    
5. python3 <path to project>/commadRunner.py

Note:
To Control brightness require this command to executed as root before setting up.
echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

To bot run as a deamon/service:
Follow this to make this run as a service
$ sudo nano /lib/systemd/system/pytel.service
Paste the following:
    
    
    [Unit]
    Description=telgram service at port 57777
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=/usr/bin/python3 <path to project>/commadRunner.py

    [Install]
    WantedBy=multi-user.target
    
$ sudo chmod 644 /lib/systemd/system/pytel.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable pytel.service
$ sudo reboot now
$ sudo systemctl status pytel.service
