from talon import actions, cron, imgui
from talon import Module, Context, actions
from talon.mac import applescript

mod = Module()

mod.mode("repeater", "Auto repeater mode")
# mod.tag("game_voip_muted", "Signals that game voice chat is muted")

ctx = Context()
ctx.matches = r"""
mode: user.repeater
"""

ctx.settings = {
    "speech.timeout": 0.02,
}

cycle_job = None

cmd_fn = None
start_fn = None
stop_fn = None

cmd = None
anti_cmd = None

delay = None
repeat_count = 0
jump_steps = 5
is_paused = False


@imgui.open(x=200, y=0)
def repeat_gui(gui: imgui.GUI):
    gui.text(f"Auto-Repeater Mode")
    gui.line()
    gui.text("")
    gui.text(f"Action: {cmd}")
    gui.text("")
    if is_paused:
        gui.line()
        gui.text("paused (say 'resume' to continue)")
        gui.text("")
    if gui.button("Stop"):
        actions.user.stop_repeat_fn()


@mod.action_class
class Actions:
    def repeater_mode_enable():
        """Enable auto repeater mode"""
        actions.mode.disable("command")
        actions.mode.enable("user.repeater")

    def repeater_mode_disable():
        """Disable auto repeater mode"""
        actions.mode.enable("command")
        actions.mode.disable("user.repeater")

    def repeat_command(cmd_name: str, speed: str, anti_cmd_name: str = None, jmp_steps: int = 5):
        """Start auto repeating a command"""
        global cycle_job, current_key, delay, cmd_fn, repeat_count, cmd, jump_steps
        global anti_cmd
        if speed == "fast":
            delay = "200ms"
        elif speed == "slow":
            delay = "900ms"
        else:
            delay = speed

        cmd = cmd_name
        anti_cmd = anti_cmd_name or None
        jump_steps = jmp_steps
        actions.user.repeater_mode_enable()

        map_command_and_hooks(cmd)

        if start_fn:
            start_fn()

        cycle_job = cron.after(delay, repeat_command_fn)
        repeat_count += 1
        repeat_gui.show()

    def stop_repeat_fn():
        """Stop auto repeating"""
        global cycle_job, repeat_count, cmd_fn, stop_fn, start_fn, jump_steps
        if cycle_job:
            print("stop_repeat")
            cron.cancel(cycle_job)

        if stop_fn:
            stop_fn()

        start_fn = None
        stop_fn = None

        cycle_job = None
        repeat_count = 0
        jump_steps = 5
        repeat_gui.hide()
        actions.user.repeater_mode_disable()

    def reverse():
        """reverse auto repeating"""
        global cmd, anti_cmd, cmd_fn
        if anti_cmd:
            cmd, anti_cmd = anti_cmd, cmd
            map_command_and_hooks(cmd)
            cmd_fn()
            if cycle_job:
                cron.cancel(cycle_job)
                cycle_job = cron.after(delay, repeat_command_fn)

    def pause():
        """pause auto repeating"""
        global cycle_job, is_paused
        if cycle_job:
            cron.cancel(cycle_job)
            cycle_job = None
            is_paused = True
        else:
            cmd_fn()
            cycle_job = cron.after(delay, repeat_command_fn)
            is_paused = False

    def slow_down():
        """Slow down repeating"""
        global delay
        delay = "900ms"

    def go_faster():
        """Speed up repeating"""
        global delay
        delay = "250ms"

    def boost(num: int):
        """Speed up repeating"""
        global cycle_job
        if cycle_job:
            cron.cancel(cycle_job)

        for _ in range(num or jump_steps):
            actions.sleep("50ms")
            cmd_fn()

        cycle_job = cron.after(delay, repeat_command_fn)

    def jump_back():
        """Execute the reverse command"""
        if anti_cmd:
            map_command_and_hooks(anti_cmd)
            cmd_fn()

    def jump_again():
        """Execute the command again"""
        if cmd:
            map_command_and_hooks(cmd)
            cmd_fn()

    def modifier_up(modifier: str):
        """Send modifier up event"""
        print("modifier_up", modifier)
        applescript.run(
            f"""
                tell application "System Events"
                    key up {modifier}
                end tell
            """)

    def modifier_down(modifier: str):
        """Send modifier down event"""
        print("modifier_down", modifier)
        applescript.run(
            f"""
                tell application "System Events"
                    key down {modifier}
                end tell
            """)

    def keystroke(key: str):
        """Send keystroke"""
        applescript.run(
            f"""
                tell application "System Events"                    
                    keystroke {key}
                end tell
            """)


def map_command_and_hooks(cmd: str):
    global cmd_fn, start_fn, stop_fn
    match cmd:
        case "up":
            cmd_fn = actions.edit.up
        case "down":
            cmd_fn = actions.edit.down
        case "left":
            cmd_fn = actions.edit.left
        case "right":
            cmd_fn = actions.edit.right
        case "page_up":
            cmd_fn = actions.edit.page_up
        case "page_down":
            cmd_fn = actions.edit.page_down
        case "word_left":
            cmd_fn = actions.edit.word_left
        case "word_right":
            cmd_fn = actions.edit.word_right
        case "select_word_left":
            cmd_fn = actions.edit.extend_word_left
        case "select_word_right":
            cmd_fn = actions.edit.extend_word_right
        case "select_left":
            cmd_fn = actions.edit.extend_left
        case "select_right":
            cmd_fn = actions.edit.extend_right
        case "scroll_up":
            cmd_fn = actions.user.mouse_scroll_up
        case "scroll_down":
            cmd_fn = actions.user.mouse_scroll_down
        case "tab_next":
            cmd_fn = actions.app.tab_next
        case "tab_previous":
            cmd_fn = actions.app.tab_previous
        case "select_more":
            def cmd_fn(): return actions.user.vscode("editor.action.smartSelect.expand")
        case "select_less":
            def cmd_fn(): return actions.user.vscode("editor.action.smartSelect.shrink")
        case "focus_app_next":
            def cmd_fn():
                actions.user.keystroke("tab")

            def start_fn():
                actions.user.modifier_down("command")
                actions.sleep("50ms")

            def stop_fn():
                actions.user.modifier_up("command")
        case "focus_app_previous":
            def cmd_fn():
                actions.user.keystroke("tab using shift down")

            def start_fn():
                actions.user.modifier_down("command")

            def stop_fn():
                actions.user.modifier_up("command")
        case "go_tab_next":
            def cmd_fn():
                actions.user.keystroke("tab")

            def stop_fn():
                actions.user.modifier_up("control")
        case "go_tab_previous":
            def cmd_fn():
                actions.user.keystroke("tab using shift down")

            def stop_fn():
                actions.user.modifier_up("control")


def repeat_command_fn():
    global cmd_fn, repeat_count, delay, cycle_job
    print("cb last:", repeat_count)
    repeat_count += 1

    if repeat_count > 300:
        actions.user.stop_repeat_fn()
        return
    if cmd_fn:
        cmd_fn()
        cycle_job = cron.after(delay, repeat_command_fn)
