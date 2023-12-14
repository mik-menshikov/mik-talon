import os
import traceback
from talon import actions, app, speech_system, cron

RECORDINGS_FOLDER = "recordings"

talon_home = actions.path.talon_home()


def get_last_voice_files(max: int):
    try:
        recordings_path = os.path.join(talon_home, RECORDINGS_FOLDER)
        all_files = os.listdir(recordings_path)
        all_files.sort(key=lambda x: os.path.getctime(
            os.path.join(recordings_path, x)), reverse=True)

        return [os.path.join(recordings_path, file) for file in all_files[:max]]
    except FileNotFoundError:
        traceback.print_exc()
        return []


def get_last_voice_file():
    files = get_last_voice_files(1)
    if len(files) > 0:
        return files[0]


def repeat_wake():
    path = get_last_voice_file()
    actions.speech.enable()

    if path:
        actions.sleep("200ms")
        actions.speech.replay(path)
    else:
        print("Voice file not found")
        app.notify("Voice file not found")


def pre_phrase(e):
    if actions.speech.enabled():
        return

    cmd = e["text"]

    if cmd == ["wake", "up"]:
        cron.after("200ms", actions.speech.enable)
        return

    if cmd[:2] == ["wake", "up"]:
        actions.speech.record_flac()
        cron.after("200ms", repeat_wake)


speech_system.register("pre:phrase", pre_phrase)
