import os
from talon import Module, actions, speech_system, cron

talon_home = actions.path.talon_home()

mod = Module()


def get_last_voice_files(max: int):
    recordings_path = os.path.join(talon_home, "recordings")
    all_files = os.listdir(recordings_path)
    all_files.sort(key=lambda x: os.path.getctime(
        os.path.join(recordings_path, x)), reverse=True)

    return [os.path.join(recordings_path, file) for file in all_files[:max]]


def get_last_voice_file():
    files = get_last_voice_files(1)
    if len(files) > 0:
        return files[0]


def repeat_wake():
    path = get_last_voice_file()
    actions.speech.enable()
    actions.sleep("200ms")
    actions.speech.replay(path)


def pre_phrase(e):
    cmd = e["text"]
    if actions.speech.enabled():
        return

    if not actions.speech.enabled() and (cmd == ["wake", "up"]):
        cron.after("200ms", actions.speech.enable)
        return

    if not actions.speech.enabled() and (e["text"][:2] == ["wake", "up"]):
        actions.speech.record_flac()
        cron.after("200ms", repeat_wake)


speech_system.register("pre:phrase", pre_phrase)
