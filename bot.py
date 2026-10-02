import os
import discord
from discord import app_commands
from discord.ui import Button, View
from dotenv import load_dotenv
from datetime import datetime
import database as db
import calendar_sync

load_dotenv()
TOKEN = os.getenv("")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class AttendanceBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = AttendanceBot()

class AttendanceView(View):
    def __init__(self, session_id: int):
        super().__init__(timeout=None)
        self.session_id = session_id

    @discord.ui.button(label="Attending", style=discord.ButtonStyle.green, custom_id="attending")
    async def attending(self, interaction: discord.Interaction, button: Button):
        await self._handle(interaction, "attending")

    @discord.ui.button(label="Maybe", style=discord.ButtonStyle.grey, custom_id="maybe")
    async def maybe(self, interaction: discord.Interaction, button: Button):
        await self._handle(interaction, "maybe")

    @discord.ui.button(label="Not Attending", style=discord.ButtonStyle.red, custom_id="not_attending")
    async def not_attending(self, interaction: discord.Interaction, button: Button):
        await self._handle(interaction, "not_attending")

    async def _handle(self, interaction: discord.Interaction, status: str):
        db.set_attendance(
            self.session_id,
            str(interaction.user.id),
            interaction.user.display_name,
            status
        )
        await interaction.response.send_message(
            f"You’re now marked as **{status.replace('_', ' ')}**.",
            ephemeral=True
        )
        await update_attendance_message(interaction.message, self.session_id)

async def update_attendance_message(message: discord.Message, session_id: int):
    session = db.get_session(session_id)
    attendees = db.get_attendance(session_id)

    attending = [a["username"] for a in attendees if a["status"] == "attending"]
    maybe = [a["username"] for a in attendees if a["status"] == "maybe"]
    not_attending = [a["username"] for a in attendees if a["status"] == "not_attending"]

    # Format time in UK style: DD/MM/YYYY at HH:MM
    try:
        dt = datetime.fromisoformat(session["start_time"])
        display_when = dt.strftime("%d/%m/%Y at %H:%M")
    except Exception:
        display_when = session["start_time"]

    embed = discord.Embed(
        title=session["title"],
        description=session["description"] or "No description",
        color=discord.Color.blue()
    )
    embed.add_field(name="When", value=display_when, inline=False)
    embed.add_field(
        name=f"✅ Attending ({len(attending)})",
        value="\n".join(attending) or "—",
        inline=True
    )
    embed.add_field(
        name=f"❓ Maybe ({len(maybe)})",
        value="\n".join(maybe) or "—",
        inline=True
    )
    embed.add_field(
        name=f"❌ Not Attending ({len(not_attending)})",
        value="\n".join(not_attending) or "—",
        inline=True
    )
    embed.set_footer(text=f"Session ID: {session_id}")

    await message.edit(embed=embed, view=AttendanceView(session_id))

@client.tree.command(name="session", description="Create a new D&D session")
@app_commands.describe(
    title="Session title",
    date="Date in UK format (DD/MM/YYYY) e.g. 05/10/2026",
    time="Time in 24-hour format (HH:MM) e.g. 19:00",
    description="Optional description"
)
async def create_session(
    interaction: discord.Interaction,
    title: str,
    date: str,
    time: str,
    description: str = ""
):
    try:
        # Parse UK date (DD/MM/YYYY) + time (HH:MM)
        start = datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
        start_iso = start.isoformat()
        # Nice UK display: 05/10/2026 at 19:00
        display_when = start.strftime("%d/%m/%Y at %H:%M")
    except ValueError:
        await interaction.response.send_message(
            "Invalid format.\n"
            "• Date must be `DD/MM/YYYY` (e.g. `05/10/2026`)\n"
            "• Time must be `HH:MM` in 24-hour format (e.g. `19:00`)",
            ephemeral=True
        )
        return

    session_id = db.create_session(title, description, start_iso)

    # Create Google Calendar event
    try:
        event_id = calendar_sync.create_event(title, description, start_iso)
        db.update_google_event_id(session_id, event_id)
    except Exception as e:
        print(f"Calendar error: {e}")

    embed = discord.Embed(
        title=title,
        description=description or "No description",
        color=discord.Color.blue()
    )
    embed.add_field(name="When", value=display_when, inline=False)
    embed.add_field(name="✅ Attending (0)", value="—", inline=True)
    embed.add_field(name="❓ Maybe (0)", value="—", inline=True)
    embed.add_field(name="❌ Not Attending (0)", value="—", inline=True)
    embed.set_footer(text=f"Session ID: {session_id}")

    view = AttendanceView(session_id)
    await interaction.response.send_message(embed=embed, view=view)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")
    db.init_db()

client.run(TOKEN)
