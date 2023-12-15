mode: user.repeater
-

slow$: user.slow_down()
fast$: user.go_faster()
(stop | done)$: user.stop_repeat_fn()
(pause | resume)$: user.pause()
change$: user.reverse()
jump [<number_small>]$: user.boost(number_small or 0)