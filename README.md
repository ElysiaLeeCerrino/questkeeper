# QuestKeeper – D&D Attendance Bot

Discord bot + web dashboard that tracks D&D session attendance and syncs events to Google Calendar.

**UK date & time format** (`DD/MM/YYYY` + `HH:MM`).

## Features

- `/session` slash command to create sessions
- Interactive attendance buttons (Attending / Maybe / Not Attending)
- Google Calendar event creation
- Simple web dashboard

---

## Hosting on Render (recommended for 24/7)

### 1. Create a Background Worker

1. Go to [Render Dashboard](https://dashboard.render.com)
2. **New +** → **Background Worker**
3. Connect the GitHub repo: `ElysiaLeeCerrino/questkeeper`
4. Settings:

| Setting | Value |
|---------|-------|
| **Name** | `questkeeper-bot` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |

### 2. Environment Variables

In the Render service → **Environment**, add these:

| Key | Value |
|-----|-------|
| `DISCORD_TOKEN` | Your Discord bot token |
| `GOOGLE_CALENDAR_ID` | `33c0b8312c6bfa3cd8039034257d42b4a41740607c34ef8d011e2593120f42fa@group.calendar.google.com` |
| `GOOGLE_CREDENTIALS_JSON` | Paste the **entire contents** of your `service-account.json` file (as one long string) |
| `FLASK_SECRET` | Any random string |

> **How to get `GOOGLE_CREDENTIALS_JSON`:**  
> Open your `service-account.json` in a text editor, copy **everything**, and paste it as the value of the environment variable.

### 3. Deploy

Click **Create Background Worker** (or **Manual Deploy** if it already exists).  
When the logs show `Logged in as QuestKeeper#...` the bot is online.

---

## Local setup (Windows)

```powershell
git clone https://github.com/ElysiaLeeCerrino/questkeeper.git
cd questkeeper
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file:

```env
DISCORD_TOKEN=your_bot_token_here
GOOGLE_CREDENTIALS=./service-account.json
GOOGLE_CALENDAR_ID=your_calendar_id@group.calendar.google.com
FLASK_SECRET=any-random-string
```

Then run:

```powershell
python bot.py
```

---

## Discord command

```
/session title:Dragon Heist Session 3 date:05/10/2026 time:19:00 description:Bring character sheets
```

- **date** → `DD/MM/YYYY`
- **time** → `HH:MM` (24-hour)

---

## Important security notes

- Never commit `.env` or `service-account.json` (they are in `.gitignore`).
- If you ever shared your Discord bot token, reset it in the [Discord Developer Portal](https://discord.com/developers/applications).
