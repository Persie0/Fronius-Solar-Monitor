#!/bin/bash
# Setup autostart for Fronius Solar Monitor on DietPi

SCRIPT_DIR="/root/Fronius-Solar-Monitor"
AUTOSTART_SCRIPT="/var/lib/dietpi/dietpi-autostart/custom.sh"
LOG_FILE="$SCRIPT_DIR/solar_monitor.log"

echo "Setting up autostart for Fronius Solar Monitor..."

# Ensure script directory exists
if [ ! -d "$SCRIPT_DIR" ]; then
    echo "Error: $SCRIPT_DIR not found! Make sure the script is in the correct location."
    exit 1
fi

# Create autostart script
cat <<EOF > "$AUTOSTART_SCRIPT"
#!/bin/bash
# DietPi-AutoStart custom script for Fronius Solar Monitor

cd "$SCRIPT_DIR" || exit 1

# Ensure config file exists
if [ ! -f "config.json" ]; then
    if [ -f "_config.json" ]; then
        cp "_config.json" "config.json"
        echo "\$(date): Created config.json from template" >> "$LOG_FILE"
    else
        echo "\$(date): ERROR - No config file found!" >> "$LOG_FILE"
        exit 1
    fi
fi

# Install dependencies if needed
if ! command -v python3 &>/dev/null; then
    echo "\$(date): Python3 not found. Installing..." >> "$LOG_FILE"
    apt-get update && apt-get install -y python3 python3-pip
fi

if [ ! -f ".packages_installed" ]; then
    echo "\$(date): Installing required packages..." >> "$LOG_FILE"
    pip3 install requests
    touch ".packages_installed"
fi

# Run script in the background
echo "\$(date): Starting solar monitor..." >> "$LOG_FILE"
python3 solar_monitor.py >> "$LOG_FILE" 2>&1 &
EOF

# Make script executable
chmod +x "$AUTOSTART_SCRIPT"

# Enable autostart in DietPi
sudo dietpi-autostart 7

echo "Autostart setup complete! Reboot to apply changes."

