

# Fronius Solar Monitor 🌞⚡

This Python script monitors solar power data from the **Fronius Solar API** and sends Telegram alerts when the battery is full or no longer full.

## Overview

**Fronius Solar Monitor** helps you optimize your solar energy consumption by alerting you when your battery reaches full capacity or drops below it. Perfect for regions where excess energy fed to the grid isn't compensated beyond certain limits.
You can also make changes and use it as part of your larger home automation system.

### How it Works
1. **Fronius Inverter** provides real-time data via the **Solar API** (e.g., battery status, power consumption, etc.).
2. **Fronius Solar Monitor** retrieves this data using the API and evaluates the battery status.
3. Based on the readings, the script sends **Telegram notifications** (battery full or not) to the user.
4. **Alerts are customizable** based on frequency and consecutive checks, reducing false positives.


## 📋 System Requirements

- **Supported Inverters**: Fronius GEN24 series
- **Operating System**: Any Python-compatible OS (Linux recommended, Windows also ok)
- **Python**: 3.6 or higher
- **Network**: Local network access to Fronius inverter


## 🔧 Installation & Setup

### Prerequisites

- Python 3.x
- A Fronius inverter with Solar API
- Telegram account

### Step 1: Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install requests  # Required for making API requests to the Fronius inverter
```

### Step 2: Enable the Fronius Solar API

The **Solar API** must be enabled on **Fronius GEN24** devices to avoid 404 errors.

#### How to Enable:

1. **Access the Fronius Web Interface**
   - Enter your Fronius inverter's IP address in a browser.
   - Find the IP through:
     - Your router's device list
     - The IP configured during installation
     - Network scanning tools
   
   ![Router](docs/router.jpg)

2. **Enable the API**
   - Navigate to **Communication → Solar API**
   - Toggle the **Solar API** setting to enabled.
   - Save your changes.
   
   ![Solar API](docs/pv.jpg)

### Step 3: Create a Telegram Bot

1. **Create Your Bot**
   - Open Telegram and search for **@BotFather**
   - Send `/newbot` and follow the instructions.
   - Save the **Bot Token** provided.

2. **Configure Chat ID**
   - For a **group chat**: Add your bot to a group.
   - For a **private chat**: Start a conversation with your bot.
   - Send any message to the bot.
   - Get your **Chat ID** by opening:
     ```
     https://api.telegram.org/bot<TOKEN>/getUpdates
     ```
   - **Note**: Group chat IDs are negative numbers; private chat IDs are positive.

   ![Response](docs/tgchatid.png)

### Step 4: Configure the Application

Rename `_config.json` to `config.json` and configure it with your settings:

```json
{
{
  "telegram_token": "6467835642:AAAAAl99Ue14-e2cPqF79KSdOol5-aTr123",
  "chat_id": "-1048737232455",
  "solar_api_ip": "192.168.1.131",
  "check_interval_min": 1,
  "consecutive_full_checks": 1,
  "consecutive_not_full_checks": 4,
  "language": "en"
}
}
```

#### Configuration Parameters:

| Parameter | Description | Recommended Value |
|-----------|-------------|-------------------|
| `telegram_token` | Your Telegram bot token | - |
| `chat_id` | Target chat ID for notifications | Negative for groups, positive for private chats |
| `solar_api_ip` | IP address of Fronius inverter | Local network IP of inverter |
| `check_interval_min` | Time between checks (minutes) | 1-5 |
| `consecutive_full_checks` | Readings needed before "battery full" alert | 1-3 |
| `consecutive_not_full_checks` | Readings needed before "battery not full" alert | 2-5 |
| `language` | Notification language | "en" or "de" |

> **Note**: Higher `consecutive_checks` values reduce false alerts but increase notification delay.

### Step 5: Run the Monitor

#### Manual Execution

To run the script manually:

```bash
python solar_monitor.py
```

#### Automatic Startup on Raspberry Pi (DietPi)

For a headless setup on Raspberry Pi running DietPi or (maybe) also other Linux distributions:

1. **Install DietPi**: Download from [dietpi.com](https://dietpi.com/docs/install/).

2. **Access via SSH in Terminal**:
   ```bash
   ssh root@192.168.1.132  # Replace with your Pi's IP
   ```

3. **Install Git and Python** via `dietpi-software` (or your package manager if using a different Linux distribution).
   
4. **Clone the repository** and navigate to the project directory:

   ```bash
   git clone https://github.com/Persie0/Fronius-Solar-Monitor.git
   cd Fronius-Solar-Monitor
   ```

5. **Verify the project directory**:
   To ensure you're in the correct directory, run the following command:
   
   ```bash
   pwd
   ```
   
   If the output is **not** `/root/Fronius-Solar-Monitor`, you will need to update the `PROJECT_DIR` variable in the setup configuration. Edit the script to reflect the correct path.

   Example:
   ```bash
   nano /otherpath/Fronius-Solar-Monitor/setup_autostart.sh
   ```

   Update the line:
   ```bash
   PROJECT_DIR="/otherpath/Fronius-Solar-Monitor"
   ```


6. **Setup Auto-Start**:
   Simply run the setup script included in the repository:
   ```bash
   sudo bash setup_autostart.sh 
   ```

7. **Configure the bot**:
   Edit the `config.json` file to include your bot's token, chat ID, and inverter's IP address.
   ```bash
   nano config.json
   ```
   then copy and paste your configured config.json into it. Then Ctrl+O Enter and Ctrl+X.

8. **Restart to test**:
   ```bash
   sudo systemctl restart solar_monitor
   ```
   now you should already get a TG notification. 
   > **Note**: If you did not get an notification, to check for errors, run:
   ```bash
   tail -f /root/Fronius-Solar-Monitor/solar_monitor.log
   ```
   And if you really want to test it run:
   ```bash
   sudo reboot
   ```


---

## 📡 Data Monitoring & API

### Example API Request

To manually check your system's status, enter in your browser:

```
http://192.168.1.131/solar_api/v1/GetPowerFlowRealtimeData.fcgi
```

(Replace with your inverter's IP)

### Sample API Response:

```json
{
  "Body": {
    "Data": {
      "Inverters": {
        "1": {
          "Battery_Mode": "battery full",
          "P": 4201.64,
          "SOC": 100
        }
      },
      "Site": {
        "P_Grid": 740.7,
        "P_Load": -4942.34,
        "P_PV": 4298.14,
        "rel_Autonomy": 85.01,
        "rel_SelfConsumption": 100
      }
    }
  },
  "Head": {
    "Status": { "Code": 0 },
    "Timestamp": "2025-02-18T14:50:13+00:00"
  }
}
```

### Data Visualization

#### Web Interface
![Web Interface](docs/webui.jpg)

#### API Response Values Explained

| Field               | Description |
|---------------------|-------------|
| `Battery_Mode`      | Battery state (e.g., "battery full") |
| `SOC`               | Battery state of charge (percentage) |
| `P_Grid`            | Power from/to the grid (positive = importing, negative = exporting) |
| `P_Load`            | Power consumption (negative values mean energy usage) |
| `P_PV`              | Solar power generation |
| `rel_Autonomy`      | Percentage of energy used from your own sources |
| `rel_SelfConsumption`| Percentage of solar energy used locally |

---

## 📚 Additional Resources

For detailed API documentation:

- [fronius-json-tools](https://github.com/akleber/fronius-json-tools)
- [Fronius Solar API Documentation (PDF)](docs/docs.pdf)

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 Error when accessing the Solar API | Ensure the Solar API is enabled on your Fronius inverter and you're using the correct IP. |
| No Telegram message received | Double-check the **Bot Token** and **Chat ID** in `config.json`. Ensure the bot is correctly added to the group or conversation. |
| Data not updating | Make sure the inverter's IP is correct and accessible from your Python script. Test with `ping` or use `curl` to manually check if the API is responding. |
| Script Crashes | Run the script in debug mode by adding `-v` for more verbose logging. Check the logs in `/var/log/solar_monitor.log` for detailed errors. |

---


## 💡 FAQ

### **Q: Can I use the Solar Monitor with other inverters?**
A: Currently, the Solar Monitor supports only **Fronius GEN24** inverters. However, you can easily also change the code for your inverter if it can also provide information via an API.
What you need for that (doable even for a non programmer person):
- find via an internet search wheter an API is available for you model
- enter the API url and response togheter with the solar_monitor.py script into e.g. ChatGPT or similar and say it should change it

---

**Happy Solar Monitoring! 🌞⚡**

