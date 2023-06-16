#!/bin/bash
# Bash file to create a systemd service for the application
sudo touch /etc/systemd/system/gp2040-flasher.service

echo "[Unit]
Description=GP2040-Flasher
After=network.target

[Service]
ExecStart=sudo /usr/bin/python3 /home/pi/GP2040-Flasher-Pi/main.py
WorkingDirectory=/home/pi/GP2040-Flasher-Pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/gp2040-flasher.service

sudo systemctl daemon-reload
sudo systemctl enable gp2040-flasher.service
