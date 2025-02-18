# Fronius Solar Monitor

This Python script monitors solar power data from the **Fronius Solar API** and sends Telegram alerts when the battery is full or no longer full.

## 🌍 Why This Project?

In some regions (like mine), feeding excess solar energy into the grid beyond a certain limit results in no compensation. This script helps monitor energy usage, enabling you to turn devices on or off accordingly, optimizing energy consumption. You can also integrate this code into your own automation projects.

## 🚀 Features

- Dynamic configuration via `config.json`
- Automatic Telegram notifications
- Logging for debugging and monitoring

---

## 🔧 Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install requests
```

### 2️⃣ Enable the Fronius Solar API

The **Solar API** must be enabled on **Fronius GEN24** devices. If disabled, API requests return a **404 error** with the message: _"Solar API disabled by customer config."_

#### 🔹 How to Enable the Solar API:

1. **Access the Fronius Web Interface:**
   - Open a browser and enter your Fronius inverter's IP address. You can find this IP by:
     - Checking your **router's web interface** (look for the inverter in the device list).
     - Using the IP set during installation.
     - Scanning your network with a tool or app.
   
   ![Router](docs/router.jpg)

2. **Enable the API:**
   - Navigate to **Communication → Solar API**.
   - Enable the **Solar API**.
   - Save your settings.
   
   ![Solar API](docs/pv.jpg)

---

### 3️⃣ Create a Telegram Bot

A more detailed tutorial is available [here](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot` and follow the setup instructions.
3. Copy the **Bot Token** and paste it into `config.json`.
4. Add your bot to a group and retrieve the **Chat ID** by opening the following URL in your browser (replace `<TOKEN>` with your bot token):

   ```bash
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
   
   ![Response](docs/tgchatid.png)

#### ➡️ Sending Messages to a Private Chat Instead of a Group

1. Start a private chat with your bot.
2. Send any message.
3. Retrieve your chat ID using:

   ```bash
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```

4. Copy the chat ID (a **positive number**; group IDs are negative).
5. Update `config.json` with your personal chat ID:

   ```json
   {
     "telegram_token": "your-telegram-bot-token",
     "chat_id": "your-personal-chat-id",
     "solar_api_ip": "xxx.xxx.xxx.xxx",
     "check_interval_min": 1
   }
   ```

---

### 4️⃣ Configure `config.json`

Edit `config.json` to match your setup:

```json
{
  "telegram_token": "6467835642:AAAAAl99Ue14-e2cPqF79KSdOol5-aTr123",
  "chat_id": "-1048737232455",
  "solar_api_ip": "192.168.1.131",
  "check_interval_min": 1
}
```

### 5️⃣ Run the Script

- Rename `_config.json` to `config.json` (remove the leading underscore).
- Execute the script:

```bash
python solar_monitor.py
```

---

## 📡 Example API Response

To check your Fronius inverter's power data, enter the following URL in your browser (replace `192.168.1.131` with your inverter's IP):

```bash
http://192.168.1.131/solar_api/v1/GetPowerFlowRealtimeData.fcgi
```

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

---

## 📜 API Documentation

For additional API requests and a detailed reference, check out:
- **[fronius-json-tools](https://github.com/akleber/fronius-json-tools)**
- **[Fronius Solar API Docs (PDF)](docs/docs.pdf)**

### 🔹 Web Interface Screenshot

![Web Interface](docs/webui.jpg)

### 🔹 API Response Equivalent

![API Response](docs/jsonmarked.jpg)

---

## 🛠️ Troubleshooting

- Ensure your **API IP address** is correct.
- Verify your Telegram bot is added to the correct group or chat.
- If you get a **404 error**, check that the **Solar API is enabled** in the Fronius Web UI.

**Happy Monitoring! 🌞⚡**

