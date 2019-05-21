from barpyrus import widgets as W

# for TimeIn
from datetime import datetime
import pytz

# for mpd
from pydbus import SessionBus


import subprocess

class Kbd(W.Label):
    def __init__(self):
        super(Kbd,self).__init__('')
        self.buttons = [1, 3]
        self.timer_interval = 1
        self.last_time = ''
        self.timeout()

    def timeout(self):
        command = "xkblayout-state print %e"
        self.label = subprocess.run(command.split(), capture_output=True).stdout.decode('utf8').strip()
        if_changed = (self.label != self.last_time)
        self.last_time = self.label
        return if_changed

    def on_click(self, b):
        if b == 1:
            command = "xkblayout-state set +1"
            subprocess.run(command.split(), capture_output=True).stdout.decode('utf8').strip()
        elif b == 3:
            command = "xkblayout-state set -1"
            subprocess.run(command.split(), capture_output=True).stdout.decode('utf8').strip()

class Mpd(W.Label):
    def __init__(self):
        super(Mpd,self).__init__('')
        self.buttons = [1, 3]
        self.timer_interval = 1
        self.last_time = ''
        self._dbus = SessionBus()
        self._bus = self._dbus.get("org.freedesktop.DBus")
        self.player = self._dbus.get('org.mpris.MediaPlayer2.mpd', "/org/mpris/MediaPlayer2")
        self.timeout()

    def timeout(self):
        self.label = self.player.PlaybackStatus
        if_changed = (self.label != self.last_time)
        self.last_time = self.label
        return if_changed

    def on_click(self, b):
        if b == 1:
            self.player.Play()
        elif b == 3:
            self.player.Pause()

class TimeIn(W.Label):
    def __init__(self, choices = "London"):
        super(TimeIn,self).__init__('')
        self.choices = choices
        self.choice = 0
        self.buttons = [1, 3]
        self.timer_interval = 1
        self.last_time = ''
        self.timeout()

    def timezone(self, tz: str) -> str:
        zone = pytz.timezone(tz)
        t = datetime.now(zone)
        return t.strftime(f"%A %B %e, %Y - %H:%M [{zone}]")

    def timeout(self):
        self.label = self.timezone(self.choices[self.choice])
        if_changed = (self.label != self.last_time)
        self.last_time = self.label
        return if_changed

    def on_click(self, b):
        if b == 1:
            self.choice = (self.choice + 1) % len(self.choices)
        elif b == 3:
            self.choice = (self.choice - 1) % len(self.choices)
