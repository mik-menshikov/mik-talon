app: vscode
win.title: /^Search/
-

focus search: user.vscode("search.action.focusQueryEditorWidget")
hunt exclude: user.vscode("search.action.focusFilesToExclude")
hunt include: user.vscode("search.action.focusFilesToInclude")
context more: user.vscode("increaseSearchEditorContextLines")
context less: user.vscode("decreaseSearchEditorContextLines")
hunt word: user.vscode("toggleSearchEditorWholeWord")
hunt expression: user.vscode("toggleSearchEditorRegex")
hunt case: user.vscode("toggleSearchEditorCaseSensitive")
next one: user.vscode("search.action.focusNextSearchResult")
previous one: user.vscode("search.action.focusPreviousSearchResult")

