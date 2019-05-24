from marconpa.core import Waveform
from marconpa.utils.conversions import dict2stringlist, list2string
from collections import OrderedDict
import attr


@attr.s
class Channel:

    waveforms = attr.ib(type = OrderedDict, default={})
    attributes = attr.ib(type= OrderedDict, default={})

    Enabled = attr.ib(type= Waveform, default=Waveform())


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
                enabled = Waveform.from_waveform_dict(data["Enabled"])
            elif type(data[i]) is dict and not i == "Enabled":
                waveforms[i] = Waveform.from_waveform_dict(wave_form_dict=data[i])
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
                fields.append("\t" * depth + str(attrib[0]) + " = ")
                fields.append("\t" * depth + "{")
                fields += attrib[1].export_as_listofstring(depth=depth + 1)
                fields.append("\t" * depth + "}")

        return fields

    def as_string(self):
        listofstrings = self.as_lisfofstrings()
        text = "\n".join(listofstrings)
        return text


