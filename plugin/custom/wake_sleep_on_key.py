from talon import actions, cron
from talon import Module, actions, cron, ui
from talon.canvas import Canvas

mod = Module()
canvas: Canvas = None


@mod.action_class
class Actions:
    def keyboard_speech_toggle():
        """Toggles speech recognition"""
        # Talon is awake
        if actions.speech.enabled():
            actions.speech.disable()
            show_mode(False)
        # In sleep mode
        else:
            actions.speech.enable()
            show_mode(True)


def show_mode(mode):
    def on_draw(c):
        c.paint.typeface = "Arial"
        # The min(width, height) is to not get gigantic size on portrait screens
        c.paint.textsize = round(min(c.width, c.height) / 4)
        text = f"listening" if mode == True else "sleep"
        rect = c.paint.measure_text(text)[1]
        x = c.x + c.width / 2 - rect.x - rect.width / 2
        y = c.y + c.height / 2 + rect.height / 2

        c.paint.style = c.paint.Style.FILL
        c.paint.color = "0000cc" if mode == True else "cc0000"
        c.draw_text(text, x, y)

        c.paint.style = c.paint.Style.STROKE
        c.paint.color = "cccccc"
        c.draw_text(text, x, y)

        cron.after("1s", canvas.close)

    screen = ui.main_screen()
    canvas = Canvas.from_rect(screen.rect)
    canvas.register("draw", on_draw)
    canvas.freeze()
