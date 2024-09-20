import os

def notify(title, text):
    os.system(f"osascript -e 'display notification \"{text}\" with title \"{title}\"'")

def play_default_sound(sound_id: str):
    os.system(f"afplay /System/Library/Sounds/{sound_id.capitalize()}.aiff")

def on_poll_update(monitor):
    notify("Poll Update", monitor.url)
    play_default_sound('funk')