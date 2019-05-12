from Marconpa.core.configs.wave_form import Waveform

from typing import Dict, Union
import attr


@attr.s(auto_attribs=True)
class Channel:


    attributes: Dict[str, Union[str, int, float, bool]]

    Enabled: Waveform

    waveforms: Dict[str, Waveform]



    @classmethod
    def parsed_channel(cls, data):
        """
        Creates Channel instance from data, which are channel contents parsed by Marconppa.core.parse.lark
        :param data: Dictionary containing data from channel
        :return: Channel instance
        """


        attributes = {}
        waveforms = {}
        for i in data.keys():
            if i == "Enabled":
                enabled = Waveform(data["Enabled"])
            elif type(data[i]) is dict and not i == "Enabled":
                waveforms[i] = Waveform(wave_form_dict=data[i])
            else:
                attributes[i] = data[i]

        return cls(Enabled=enabled, attributes=attributes, waveforms=waveforms)

    def as_lisfofstrings(self):

        fields = ["{"]
        for attrib in self.__attrs_attrs__:
            value = getattr(self, attrib.name)
            if isinstance(value, dict):
                fields += dict2stringlist(value)
            else:
                fields += dict2stringlist({attrib.name: value})
        fields.append("}")

        return fields

    def as_string(self):
        listofstrings = self.as_lisfofstrings()
        text = "\n".join(listofstrings)
        return text

def dict2stringlist(data, depth = 0):

    if depth > 0:
        lines = ["\t" * depth + "{"]
    else:
        lines = []

    depth += 1
    for i in data.keys():
        if isinstance(data[i], dict):
            lines.append("\t" * depth + "{0} = ".format(i))
            lines = lines + dict2stringlist(data[i], depth=depth)
        elif isinstance(data[i], list):
            lines.append("\t" * depth + "{0} = {1}".format(i, list2string(data[i])))
        elif isinstance(data[i], Waveform):
            lines.append("\t" * depth + "{0} = ".format(i))
            lines = lines + dict2stringlist(data[i].export_waveform(), depth=depth)
        else:
            lines.append("\t" * depth + "{0} = {1}".format(i, data[i]))


    depth -= 1

    if depth > 0:
        lines.append("\t" * depth + "}")

    return lines

def list2string(data):

    text = "{"

    for i in data:
        text += "{0} ".format(i)

    text += "}"

    return text

if __name__ == "__main__":
    from Marconpa.examples.example import parse_density

    conf = parse_density()


    fch = Channel.parsed_channel(conf["FeedbackChannel"])
    a = fch.as_lisfofstrings()
    b = "\n".join(a)

    with open("test.txt", "w") as filesave:
        filesave.write(b)
