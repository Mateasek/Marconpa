from marconpa.core.configs.wave_form import Waveform
from marconpa.core.utils.conversions import dict2stringlist, list2string
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

    def as_lisfofstrings(self, depth=0):

        fields = []
        for attrib in self.attributes.items():
            if isinstance(attrib[1], list):
                fields += [
                    "\t" * depth + str(attrib[0]) + " = " + list2string(attrib[1])
                ]
            else:
                fields += dict2stringlist({attrib[0]: attrib[1]}, depth=depth)

        fields.append("\t" * depth + "Enabled = ")
        fields.append("\t" * depth + "{")
        fields += self.Enabled.export_as_listofstring(depth=depth + 1)
        fields.append("\t" * depth + "}")

        for attrib in self.waveforms.items():
            if isinstance(attrib[1], Waveform):
                fields.append("\t" * depth + str(attrib[0]))
                fields.append("\t" * depth + "{")
                fields += attrib[1].export_as_listofstring(depth=depth + 1)
                fields.append("\t" * depth + "}")

        return fields

    def as_string(self):
        listofstrings = self.as_lisfofstrings()
        text = "\n".join(listofstrings)
        return text


if __name__ == "__main__":
    from marconpa.examples.example import parse_density

    conf = parse_density()

    fch = Channel.parsed_channel(conf["FeedbackChannel"])
    a = fch.as_lisfofstrings()
    b = "\n".join(a)

    with open("test.txt", "w") as filesave:
        filesave.write(b)
