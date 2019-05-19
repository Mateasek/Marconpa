from Marconpa.core.parser.lark import MarteConfigParser


def parse_density():
    parser = MarteConfigParser()

    confpath = "/home/maajk/Python/packages/Marconpa/Marconpa/examples/Density"

    with open(confpath, "r") as filecont:
        density = parser.parse_config(config_text=filecont.read())

    return density
