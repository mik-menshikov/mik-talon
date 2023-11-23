import time
from talon import Module, actions, cron, speech_system, ui
from talon.canvas import Canvas

canvas: Canvas = None
mod = Module()

last_phrase_time = None
timeout_job = None
timeout = mod.setting("sleep_timeout_min", int, default=-1).get()


def check_timeout():
    global last_phrase_time, timeout_job, timeout
    if last_phrase_time and time.perf_counter() - last_phrase_time > timeout * 60:
        actions.speech.disable()
        show_mode(False)
        cron.cancel(timeout_job)
    else:
        timeout_job = cron.after("5s", check_timeout)


def post_phrase(e):
    global last_phrase_time, timeout_job, timeout
    if actions.speech.enabled():
        cron.cancel(timeout_job)
        print("timeout", f"{timeout}s")
        timeout_job = cron.after(f"{timeout * 60}s", check_timeout)
        last_phrase_time = time.perf_counter()


def show_mode(mode):
    def on_draw(c):
        c.paint.typeface = "Arial"
        c.paint.textsize = round(min(c.width, c.height) / 5)
        text = f"on" if mode == True else "sleeping"
        rect = c.paint.measure_text(text)[1]
        x = c.x + c.width / 2 - rect.x - rect.width / 2
        y = c.y + c.height / 2 + rect.height / 2

        c.paint.style = c.paint.Style.FILL
        c.paint.color = "0000cc" if mode == True else "cc0000"
        c.draw_text(text, x, y)

        c.paint.style = c.paint.Style.STROKE
        c.paint.color = "bbbbbb"
        c.draw_text(text, x, y)

        cron.after("1s", canvas.close)

    screen = ui.main_screen()
    canvas = Canvas.from_rect(screen.rect)
    canvas.register("draw", on_draw)
    canvas.freeze()


if timeout > 0:
    speech_system.register("post:phrase", post_phrase)
