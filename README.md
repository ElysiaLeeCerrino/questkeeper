# QuestKeeper – D&D Attendance Bot

Discord bot + web dashboard that tracks D&D session attendance and syncs events to Google Calendar.

**UK date & time format** (`DD/MM/YYYY` + `HH:MM`).

## Features

- `/session` slash command to create sessions
- Interactive attendance buttons (Attending / Maybe / Not Attending)
- Google Calendar event creation
- Simple web dashboard

## Setup (Windows)

1. Make sure Python is installed from [python.org](https://www.python.org) (tick **Add to PATH**).

2. Clone this repository and open a terminal in the folder:

```powershell
git clone https://github.com/ElysiaLeeCerrino/questkeeper.git
cd questkeeper
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Create a `.env` file (copy from the example below) and fill in your values:

```env
DISCORD_TOKEN=your_bot_token_here
GOOGLE_CREDENTIALS=./service-account.json
GOOGLE_CALENDAR_ID=your_calendar_id@group.calendar.google.com
FLASK_SECRET=any-random-string
```

4. Place your Google service-account JSON file in the project folder as `service-account.json`.

5. Run the bot:

```powershell
python bot.py
```

6. (Optional) Run the web dashboard in a second terminal:

```powershell
python web.py
```

Then open http://localhost:8080

## Discord command

```
/session title:Dragon Heist Session 3 date:05/10/2026 time:19:00 description:Bring character sheets
```

- **date** → `DD/MM/YYYY`
- **time** → `HH:MM` (24-hour)

## Important security notes

- Never commit the `.env` or `service-account.json` files (they are already in `.gitignore`).
- If you ever shared your Discord bot token, reset it in the [Discord Developer Portal](https://discord.com/developers/applications).
