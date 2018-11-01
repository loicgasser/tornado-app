from handlers.draft import DraftHandlerGet, DraftHandlerPost


url_patterns = [
    (r"/draft", DraftHandlerPost),
    (r"/draft/([a-f\d]{24})", DraftHandlerGet),
]