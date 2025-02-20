#!/bin/bash

# Define variables
PROJECT_DIR="/root/Fronius-Solar-Monitor"
SERVICE_NAME="solar_monitor"
SCRIPT_PATH="$PROJECT_DIR/solar_monitor.py"
LOG_FILE="$PROJECT_DIR/solar_monitor.log"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

# Step 1: Create the systemd service file with a dependency on network-online.target
echo "Creating systemd service file..."

cat << EOF > $SERVICE_FILE
[Unit]
Description=Fronius Solar Monitor
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_PATH
WorkingDirectory=$PROJECT_DIR
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# Step 2: Reload systemd, enable and start the service
echo "Reloading systemd and starting the service..."

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Step 3: Verify the service is running
echo "Verifying if the service is running..."
systemctl status $SERVICE_NAME

# Step 4: Inform the user
echo "Solar Monitor setup complete! The service is now running."
echo "To check logs, use: journalctl -u $SERVICE_NAME -f"
echo "To restart the service, use: sudo systemctl restart $SERVICE_NAME"
echo "To stop the service, use: sudo systemctl stop $SERVICE_NAME"
