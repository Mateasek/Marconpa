import attr
from Marconpa.core.configs.channel import Channel

@attr.s(auto_attribs=True)
class ConfigFile:

    ProgrammedChannel: Channel
    FeedbackChannel: Channel
    FeedforwardChannel: Channel

    name = ""

    @classmethod
    def from_parsed(cls, data):

        return cls(ProgrammedChannel=Channel.parsed_channel(data["ProgrammedChannel"]),
                   FeedbackChannel=Channel.parsed_channel(data["FeedbackChannel"]),
                   FeedforwardChannel=Channel.parsed_channel(data["FeedforwardChannel"]))

    def as_listofstrings(self):
        lisofstrings = []
        for attribute in self.__attrs_attrs__:
            if attribute.type is Channel:
                value = getattr(self, attribute.name)
                lisofstrings.append(attribute.name)
                lisofstrings += value.as_lisfofstrings()
                lisofstrings.append("")

        return lisofstrings

    def as_string(self):
        lisofstrings = self.as_listofstrings()
        text = "\n".join(lisofstrings)
        return text


@attr.s(auto_attribs=True)
class Density(ConfigFile):

    _name: str = "Density"






if __name__ == "__main__":
    from Marconpa.examples.example import parse_density

    conf = parse_density()

    dens = Density.from_parsed(conf)

    with open("test.txt", "w") as filesave:
        filesave.write(dens.as_string())
