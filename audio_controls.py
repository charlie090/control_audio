# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from typing import Any, Callable, List, Optional, Tuple

from anki.sound import AVTag, SoundOrVideoTag
from aqt import gui_hooks, mw
from aqt.sound import (
    MpvManager,
    SimpleMplayerSlaveModePlayer,
    SimpleProcessPlayer,
    SoundOrVideoPlayer,
    av_player,
)

import aqt
from aqt.utils import tooltip
from PyQt5.QtWidgets import QAction

# Configs
audio_speed = 1.0
show_notif = True

# Play files faster in mpv/mplayer
######################################


def set_speed(player: Any, speed) -> None:
    if isinstance(player, MpvManager):
        player.set_property("speed", speed)
        tooltip("Set audio speed to " + f"{speed:.2f}")
    elif isinstance(player, SimpleMplayerSlaveModePlayer):
        player.command("speed_set", speed)
        tooltip("Set audio speed to " + f"{speed:.2f}")


# automatically play fast


def did_begin_playing(player: Any, tag: AVTag) -> None:
    # mplayer seems to lose commands sent to it immediately after startup,
    # so we add a delay for it - an alternate approach would be to adjust
    # the command line arguments passed to it
    if isinstance(player, SimpleMplayerSlaveModePlayer):
        mw.progress.timer(500, lambda: set_speed(player, audio_speed), False)
    else:
        set_speed(player, audio_speed)


gui_hooks.av_player_did_begin_playing.append(did_begin_playing)


def apply_audio_speed(player: Any, speed: float) -> None:

    if isinstance(player, MpvManager):
        aqt.sound.av_player.current_player.stop()
        player.set_property("speed", speed)
    elif isinstance(player, SimpleMplayerSlaveModePlayer):
        aqt.sound.av_player.current_player.stop()
        player.command("speed_set", speed)


def increase_audio_speed():
    #audio_speed = min(4.0, audio_speed + 0.1)
    global audio_speed
    audio_speed += 0.1
    if show_notif:
        tooltip("Increase audio speed by 0.1. Current Speed: " + f"{audio_speed:.1f}")
    apply_audio_speed(av_player.current_player, audio_speed)


def decrease_audio_speed():
    #audio_speed = max(0.1, audio_speed - 0.1)
    global audio_speed
    audio_speed -= 0.1
    if show_notif:
        tooltip("Decrease audio speed by 0.1. Current Speed: " + f"{audio_speed: .1f}")
    apply_audio_speed(av_player.current_player, audio_speed)


def stop_audio():
    if show_notif:
        tooltip("Stop audio.")
    stopping_audio(av_player.current_player)


def stopping_audio(player):
    if isinstance(player, MpvManager):
        aqt.sound.av_player.current_player.stop()

    elif isinstance(player, SimpleMplayerSlaveModePlayer):
        aqt.sound.av_player.current_player.stop()

# shortcut keys


#def on_shortcuts_change(state: str, shortcuts: List[Tuple[str, Callable]]) -> None:
#    if state == "review":
#        shortcuts.append(("8", lambda: set_speed(av_player.current_player, 0.75)))
#        shortcuts.append(("[", lambda: set_speed(av_player.current_player, audio_speed - 0.1)))
#        shortcuts.append(("]", lambda: set_speed(av_player.current_player, audio_speed + 0.1)))

#gui_hooks.state_shortcuts_will_change.append(on_shortcuts_change)

# Play .ogg files in the external program 'myplayer'
########################################################


class MyPlayer(SimpleProcessPlayer, SoundOrVideoPlayer):
    args = ["myplayer"]

    def rank_for_tag(self, tag: AVTag) -> Optional[int]:
        if isinstance(tag, SoundOrVideoTag) and tag.filename.endswith(".ogg"):
            return 100
        return None


av_player.players.append(MyPlayer(mw.taskman))

afc = mw.form.menuTools.addMenu("Audio Control")

# slower audio speed
#action = QAction("Slower audio speed", mw)
#action.setShortcut("8")
#action.triggered.connect(set_speed(av_player.current_player, 0.75))
#afc.addAction(action)

# decrease audio speed
action = QAction("Decrease audio speed", mw)
action.setShortcut("[")
action.triggered.connect(decrease_audio_speed)
afc.addAction(action)

# increase audio speed
action = QAction("Increase audio speed", mw)
action.setShortcut("]")
action.triggered.connect(increase_audio_speed)
afc.addAction(action)

# stop audio
action = QAction("Stop audio", mw)
action.setShortcut("8")
action.triggered.connect(stop_audio)
afc.addAction(action)