# -1 because we are repeating, so the initial command counts as one
<user.ordinals>: core.repeat_command(ordinals - 1)
<number_small> times: core.repeat_command(number_small - 1)
(repeat that | twice | more): core.repeat_command(1)
more <number_small> [times]: core.repeat_command(number_small)

(repeat phrase | again) [<number_small> times]:
    core.repeat_partial_phrase(number_small or 1)

key(f14): core.repeat_command(1)