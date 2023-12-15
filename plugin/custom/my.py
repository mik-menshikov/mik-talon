from talon import actions, cron, imgui
from talon import Module, actions, cron, ui
from talon.canvas import Canvas
from talon.mac import applescript

mod = Module()


@imgui.open(x=700, y=0)
def gui_wheel(gui: imgui.GUI):
    gui.text(f"Cycle Mode")
    gui.line()
    if gui.button("Tab cycle stop"):
        actions.user.tab_cycle_stop()


@mod.action_class
class Actions:
    # def keyboard_speech_toggle():
    #     """Toggles speech recognition"""
    #     # Talon is awake
    #     if actions.speech.enabled():
    #         actions.speech.disable()
    #         show_mode(False)
    #     # In sleep mode
    #     else:
    #         actions.speech.enable()
    #         show_mode(True)

    def tab_cycle():
        """Cycle through tabs"""
        global cycle_job
        cycle_job = cron.interval("700ms", continuous_tab)
        gui_wheel.show()
        actions.key(f"tab")

    def tab_cycle_stop():
        """Stop tab cycling"""
        global cycle_job
        if cycle_job:
            cron.cancel(cycle_job)
        cycle_job = None
        gui_wheel.hide()


def continuous_tab():
    actions.key(f"tab")


def on_hiss(active):
    print("hiss", active)
    # if active:
    actions.core.repeat_command(1)
