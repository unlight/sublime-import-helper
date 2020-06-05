import re


def identifier_name(text):
    return camelcase(text)


# https://github.com/ecrmnn/camelcase
def camelcase(*arguments):
    if type(arguments[0]) == list:
        # Arguments passed as list
        string = "_".join(arguments[0])
    elif len(arguments) != 1:
        # Multiple arguments passed (variadict)
        string = "_".join(list(arguments))
    else:
        # Argument was a string
        string = arguments[0]

    items = re.split(r"\-|\_|\s", string)
    items = list(filter(None, items))

    titleCased = map(lambda item: item.lower().title(), items[1:])

    return items[0].lower() + "".join(titleCased)
