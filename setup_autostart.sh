#!/bin/bash
# Setup autostart for Fronius Solar Monitor using Crontab @reboot

SCRIPT_DIR="/root/Fronius-Solar-Monitor"
LOG_FILE="$SCRIPT_DIR/solar_monitor.log"
CRON_JOB="@reboot sleep 30 && cd $SCRIPT_DIR && python3 solar_monitor.py >> $LOG_FILE 2>&1 &"

echo "Setting up Crontab autostart for Fronius Solar Monitor..."

# Ensure script directory exists
if [ ! -d "$SCRIPT_DIR" ]; then
    echo "Error: $SCRIPT_DIR not found! Make sure the script is in the correct location."
    exit 1
fi

# Ensure config file exists
if [ ! -f "$SCRIPT_DIR/config.json" ]; then
    if [ -f "$SCRIPT_DIR/_config.json" ]; then
        cp "$SCRIPT_DIR/_config.json" "$SCRIPT_DIR/config.json"
        echo "$(date): Created config.json from template" >> "$LOG_FILE"
    else
        echo "$(date): ERROR - No config file found!" >> "$LOG_FILE"
        exit 1
    fi
fi

# Install dependencies if needed
if ! command -v python3 &>/dev/null; then
    echo "$(date): Python3 not found. Installing..." >> "$LOG_FILE"
    apt-get update && apt-get install -y python3 python3-pip
fi

if [ ! -f "$SCRIPT_DIR/.packages_installed" ]; then
    echo "$(date): Installing required packages..." >> "$LOG_FILE"
    pip3 install requests
    touch "$SCRIPT_DIR/.packages_installed"
fi

# Add crontab job if not already added
(crontab -l 2>/dev/null | grep -Fq "$CRON_JOB") || (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Crontab autostart setup complete! Reboot to apply changes."
