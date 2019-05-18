
def dict2stringlist(data, depth = 0):

    lines = []

    for i in data.items():
        if isinstance(i[1], dict):
            lines.append("\t" * depth + "{0} = ".format(i[0]))
            lines.append("\t" * depth + "{")
            lines = lines + dict2stringlist(i[1], depth=depth+1)
            lines.append("\t" * depth + "}")
        else:
            lines.append("\t" * depth + "{0} = {1}".format(i[0], i[1]))

    return lines

def list2string(data):

    text = "{"

    for i in data:
        text += "{0} ".format(i)

    text += "}"

    return text
