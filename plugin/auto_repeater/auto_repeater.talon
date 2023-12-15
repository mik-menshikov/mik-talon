(jump | start) scroll [down]$: user.repeat_command("scroll_up", "slow", "scroll_down")
(jump | start) scroll up$: user.repeat_command("scroll_down", "slow", "scroll_up")

# Navigation: arrows
(jump | start) up$: user.repeat_command("up", "slow", "down", 15) 
(jump | start) down$: user.repeat_command("down", "slow", "up", 15)
(jump | start) left$: user.repeat_command("left", "slow", "right")
(jump | start) right$: user.repeat_command("right", "slow", "left")

# Navigation: page up/down
(jump | start) page up$: user.repeat_command("page_up", "1200ms", "page_down")
(jump | start) page down$: user.repeat_command("page_down", "1200ms", "page_up")

# Navigation: by word
(jump | start) word left$: user.repeat_command("word_left", "slow", "word_right")
(jump | start) word right$: user.repeat_command("word_right", "slow", "word_left")

# Selection
(jump | start) select word left$: user.repeat_command("select_word_left", "slow", "select_word_right")
(jump | start) select word right$: user.repeat_command("select_word_right", "slow", "select_word_left")

(jump | start) select left$: user.repeat_command("select_left", "slow", "select_right")
(jump | start) select right$: user.repeat_command("select_right", "slow", "select_left")

# Navigation: moving between tabs
(jump | start) tab next$: user.repeat_command("tab_next", "1200ms", "tab_previous")
(jump | start) tab (last | previous)$: user.repeat_command("tab_previous", "1200ms", "tab_next")

(jump | start) go tab next$: 
	user.modifier_down("control")
	user.repeat_command("go_tab_next", "750ms", "go_tab_previous")
(jump | start) go tab (last | previous)$: 
	user.modifier_down("control")
	user.repeat_command("go_tab_previous", "750ms", "go_tab_next")
	
# Navigation: moving between applications
(jump | start) focus next$: user.repeat_command("focus_app_next", "slow", "focus_app_previous")

(jump | start) select more$: user.repeat_command("select_more", "slow")
	 
# ============================== fast ==============================
(jump | start) scroll down fast$: user.repeat_command("scroll_up", "fast", "scroll_down")
(jump | start) scroll up fast$: user.repeat_command("scroll_down", "fast", "scroll_up")

(jump | start) up fast$: user.repeat_command("up", "200ms", "down")
(jump | start) down fast$: user.repeat_command("down", "200ms", "up")
(jump | start) left fast$: user.repeat_command("left", "150ms", "right")
(jump | start) right fast$: user.repeat_command("right", "150ms", "left")

(jump | start) page up fast$: user.repeat_command("page_up", "fast", "page_down")
(jump | start) page down fast$: user.repeat_command("pag4e_down", "fast", "page_up")

(jump | start) word left fast$: user.repeat_command("word_left", "fast", "word_right")
(jump | start) word right fast$: user.repeat_command("word_right", "fast", "word_left")

(jump | start) select word left fast$: user.repeat_command("select_word_left", "fast", "select_word_right")
(jump | start) select word right fast$: user.repeat_command("select_word_right", "fast", "select_word_left")

(jump | start) select left fast$: user.repeat_command("select_left", "fast", "select_right")
(jump | start) select right fast$: user.repeat_command("select_right", "fast", "select_left")

(jump | start) tab next fast$: user.repeat_command("tab_next", "750ms", "tab_previous")
(jump | start) tab (last | previous) fast$: user.repeat_command("tab_previous", "750ms", "tab_next")

(jump | start) focus next fast$: 	
	user.press_cmd()	
	user.repeat_command("focus_app_next", "fast", "focus_app_previous")

(jump | start) again: user.jump_again()
(jump | start) back: user.jump_back()
