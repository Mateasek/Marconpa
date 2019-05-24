import json
import binascii
import attr
from typing import Dict, Union, Any

# todo: do properly using typing and attr class
@attr.s(kw_only=True)
class IdHandler:
    """
    Class for handling compponent ids within dash application. It is tedious to keep track of what is connected to what
    in dash application. This handler should help to relate the component to its parenting compponent and thus make
    clearer orientation. Also, using type one can go through classes e.g. if type is waveform then we know that the
    component in some way handles something connected to waveform data.
    """

    name = attr.ib(type=str)
    parent = attr.ib(default=None)
    kind = attr.ib(type=str, default="")
    attributes = attr.ib(default={}, type=Dict[str, Union[str, dict, tuple, list, int, float]])
    callback = attr.ib(default=False, type=bool)
    callback_property = attr.ib(default="", type=str)

    @parent.validator
    def check_parent(self, attribute, value):
        if value is not None and not isinstance(value, IdHandler):
            raise ValueError("parrent has to be None or instance of IdHandler")

    @classmethod
    def from_id(cls, id):
        callback = False
        if "." in id:
            id, callback_property = str.split(id, ".")
            callback = True

        string = binascii.unhexlify(id[1::].encode("ascii")).decode("ascii")
        asdict = json.loads(string)

        if asdict["parent"] is not None:
            asdict["parent"] = cls.from_dict(asdict["parent"])

        inst = cls.from_dict(asdict)
        if callback:
            inst.callback = True
            inst.callback_property = callback_property

        return inst

    @classmethod
    def from_dict(cls, dictionary):
        if "name" not in dictionary:
            raise KeyError("Dictionary has to include key 'name' of type str")
        if isinstance(dictionary["parent"], dict):
            dictionary["parent"] = cls.from_dict(dictionary["parent"])

        newobj = cls(**dictionary)
        return newobj

    @property
    def id(self):
        content = self.as_dict()
        encoded = "a" + binascii.hexlify(json.dumps(content).encode("ascii")).decode("ascii")
        #if self.callback:
        #    encoded += ".{}".format(self.callback_property)
        return encoded

    def as_dict(self):
        asdict = {}
        for attribute in self.__attrs_attrs__:
            value =  getattr(self, attribute.name)
            if attribute.name == "parent":
                if value is not None:
                    asdict["parent"] = value.as_dict()
                else:
                    asdict["parent"] = None
            else:
                asdict[attribute.name] = value

        return asdict

if __name__ == "__main__":

    #parent = IdHandler(name="parent", kind="provider", attributes={"data":"content"})
    #child = IdHandler(name="child", parent=parent, kind="accepter", attributes={"data":"content d"})

    #d = {"name": "parent", "kind": "provider", "attributes":{"data":"content"}}
    #test = IdHandler.from_dict(d)

    tid = "a7b226e616d65223a2022706c6f74222c2022706172656e74223a207b226e616d65223a2022537057617665666f726d222c2022706172656e74223a207b226e616d65223a2022466565646261636b4368616e6e656c222c2022706172656e74223a207b226e616d65223a202244656e73697479222c2022706172656e74223a206e756c6c2c20226b696e64223a2022436f6e66696746696c65222c202261747472696275746573223a207b7d7d2c20226b696e64223a20224368616e6e656c222c202261747472696275746573223a207b7d7d2c20226b696e64223a202257617665666f726d222c202261747472696275746573223a207b7d7d2c20226b696e64223a202257617665666f726d222c202261747472696275746573223a207b7d7d.value"
    pid = IdHandler.from_id(tid)