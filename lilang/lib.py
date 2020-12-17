def column_from_index(text, token):
    last_cr = text.rfind('\n', 0, token.index)
    if last_cr < 0:
        last_cr = -1
    return token.index - last_cr
