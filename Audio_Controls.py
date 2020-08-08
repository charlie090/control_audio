import aqt.sound
from anki.hooks import addHook
from sys import platform

def writeAndFlush(bytes):
    if platform == "win32":
        # Windows
        mm = aqt.sound.mplayerManager
        if not mm:
            return
        mm.mplayer.stdin.write(bytes+b"\n")
        mm.mplayer.stdin.flush()
    else:
        # Mac
        mm = aqt.sound.mpvManager
        try:
            if bytes == b"pause":
                mm.togglePause()
            elif bytes == b"stop":
                mm.clearQueue()
            elif bytes.startswith(b"seek "):
                delta = int(bytes.split()[1])
                mm.seekRelative(delta)
        except anki.mpv.MPVCommandError:
            # attempting to seek while not playing, etc
            pass

def addKeys(keys):
    if platform == "win32":
        # Windows
        keys.append(("n", lambda: writeAndFlush(b"pause")))
        keys.append(("m", lambda: writeAndFlush(b"stop")))
        keys.append(("5", lambda: writeAndFlush(b"pause")))
        keys.append(("6", lambda: writeAndFlush(b"seek -5 0")))
        keys.append(("7", lambda: writeAndFlush(b"seek 5 0")))
        keys.append(("8", lambda: writeAndFlush(b"stop")))
    else:
        # Mac
        keys.append(("n", lambda: writeAndFlush(b"pause")))
        keys.append(("m", lambda: writeAndFlush(b"stop")))
        keys.append(("5", lambda: writeAndFlush(b"pause")))
        keys.append(("6", lambda: writeAndFlush(b"seek -5 0")))
        keys.append(("7", lambda: writeAndFlush(b"seek 5 0")))
        keys.append(("8", lambda: writeAndFlush(b"stop")))


addHook("reviewStateShortcuts", addKeys)
