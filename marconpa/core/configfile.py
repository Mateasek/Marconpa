import attr
from marconpa.core.configs.channel import Channel
from marconpa.core.configs.wave_form import Waveform
from marconpa.core.parser.lark import MarteConfigParser
from marconpa.core.utils.conversions import dict2stringlist


@attr.s(auto_attribs=True)
class ConfigFile:
    @classmethod
    def from_parsed(cls):
        pass

    def as_listofstrings(self):
        lisofstrings = []
        for attribute in self.__attrs_attrs__:
            if attribute.type is Channel:
                value = getattr(self, attribute.name)
                lisofstrings.append(attribute.name + " =")
                lisofstrings.append("{")
                lisofstrings += value.as_lisfofstrings(depth=1)
                lisofstrings.append("}")

        return lisofstrings

    def as_string(self):
        lisofstrings = self.as_listofstrings()
        text = "\n".join(lisofstrings)
        return text


@attr.s(auto_attribs=True)
class StandartConfig(ConfigFile):

    ProgrammedChannel: Channel = Channel()
    ProgrammedChannel: Channel = Channel()
    FeedbackChannel: Channel = Channel()
    FeedforwardChannel: Channel = Channel()

    @classmethod
    def from_parsed(cls, data):

        return cls(
            ProgrammedChannel=Channel.parsed_channel(data["ProgrammedChannel"]),
            FeedbackChannel=Channel.parsed_channel(data["FeedbackChannel"]),
            FeedforwardChannel=Channel.parsed_channel(data["FeedforwardChannel"]),
        )


@attr.s(auto_attribs=True)
class Density(StandartConfig):

    gam = "Density"


@attr.s(auto_attribs=True)
class FABR(StandartConfig):

    gam = "FABR"


@attr.s(auto_attribs=True)
class FABV(StandartConfig):

    gam = "FABV"


@attr.s(auto_attribs=True)
class MFPS(StandartConfig):

    gam = "MFPS"


@attr.s(auto_attribs=True)
class SFPS(StandartConfig):

    gam = "MFPS"


@attr.s(auto_attribs=True)
class WPPC(StandartConfig):

    gam = "WPPC"


@attr.s(auto_attribs=True)
class EFPS(ConfigFile):

    EFPSProgrammedChannel: Channel = Channel()
    EFPSCurrentFeedbackChannel: Channel = Channel()
    PositionFeedbackChannel: Channel = Channel()
    BvCurrentChannel: Channel = Channel()
    gam = "EFPS"

    @classmethod
    def from_parsed(cls, data):
        return cls(
            EFPSProgrammedChannel=Channel.parsed_channel(data["EFPSProgrammedChannel"]),
            EFPSCurrentFeedbackChannel=Channel.parsed_channel(
                data["EFPSCurrentFeedbackChannel"]
            ),
            PositionFeedbackChannel=Channel.parsed_channel(
                data["PositionFeedbackChannel"]
            ),
            BvCurrentChannel=Channel.parsed_channel(data["BvCurrentChannel"]),
        )


@attr.s(auto_attribs=True)
class WaveformConfig(ConfigFile):

    waveform: Waveform = Waveform()

    @classmethod
    def from_parsed(cls, data):
        return cls(waveform=Waveform.from_waveform_dict(data))

    def as_listofstrings(self):
        return self.waveform.export_as_listofstring()

    def as_string(self):
        listofstrings = self.as_listofstrings()
        string = "\n".join(listofstrings)
        return string


@attr.s(auto_attribs=True)
class TFPS(WaveformConfig):

    gam = "TFPS"


@attr.s(auto_attribs=True)
class Density2(WaveformConfig):

    gam = "Density2"


config_types = {
    "Density": Density,
    "Density2": Density2,
    "EFPS": EFPS,
    "FABR": FABR,
    "FABV": FABV,
    "MFPS": MFPS,
    "SFPS": SFPS,
    "TFPS": TFPS,
    "WPPC": WPPC,
}


def get_config_object(configtype, folderpath):

    parser = MarteConfigParser()
    with open(folderpath + "/" + configtype, "r") as of:
        parsed = parser.parse_config(of.read())

    obj = config_types[configtype].from_parsed(parsed)

    return obj


if __name__ == "__main__":

    filetoload = "/home/maajk/configs/original"
    filetosave = "/home/maajk/configs/reconstructed/"
    configs = {}

    for i in config_types.keys():
        configs[i] = get_config_object(i, filetoload)

    for i in configs.items():
        with open(filetosave + i[0], "w") as fts:
            fts.write(i[1].as_string())

    configs_exported = {}
    for key, item in config_types.items():
        configs_exported[key] = get_config_object(key, filetosave)

    if False:
        with open(filetosave+"FABR", "r") as fl:
           cont = fl.read()

        parser = MarteConfigParser()
        parsed = parser.parse_config(cont)