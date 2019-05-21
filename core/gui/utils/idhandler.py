import json
import re
import base64
import binascii

class IdHandler:
    """
    Class for handling compponent ids within dash application. It is tedious to keep track of what is connected to what
    in dash application. This handler should help to relate the component to its parenting compponent and thus make
    clearer orientation. Also, using type one can go through classes e.g. if type is waveform then we know that the
    component in some way handles something connected to waveform data.
    """

    def __init__(self, name, component_type=None, parent=None):
        self.component_type = component_type
        self.name = name
        self.parent = parent

    @classmethod
    def from_id(cls, id):
        string = binascii.unhexlify(id[1::].encode("ascii")).decode("ascii")
        asdict = json.loads(string)

        try:
            content = cls.from_dict(asdict["parent"])
        except TypeError:
            asdict["parent"] = asdict["parent"]
        else:
            asdict["parent"] = content

        return cls(**asdict)

    @classmethod
    def from_dict(cls, dictionary):

        newobj = cls(**dictionary)

        if isinstance(newobj.parent, dict):
            newobj["parent"] = cls.from_dict(newobj["parent"])

        return newobj

    @property
    def id(self):
        content = {}
        content["component_type"] = self.component_type
        content["name"] = self.name
        if isinstance(self.parent, IdHandler):
            content["parent"] = self.parent.as_dict()
        else:
            content["parent"] = self.parent

        encoded = "a" + binascii.hexlify(json.dumps(content).encode("ascii")).decode("ascii")
        return encoded

    def as_dict(self):
        content = {}
        content["component_type"] = self.component_type
        content["name"] = self.name
        if isinstance(self.parent, IdHandler):
            content["parent"] = self.parent.as_dict()
        else:
            content["parent"] = self.parent

        return content


if __name__ == "__main__":

    comp2 = IdHandler(component_type="channel", name="SP", )
    comp1 = IdHandler(component_type="waveform", name="table", parent=comp2)

    id1 = comp1.id
    id2 = comp2.id

    a = IdHandler.from_id(id1)
    b = IdHandler.from_id(id2)