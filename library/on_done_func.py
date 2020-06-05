# Return a function which is used with sublime list picking.
def on_done_func(choices, func):
    def on_done(index):
        if index >= 0:
            return func(choices[index])

    return on_done
