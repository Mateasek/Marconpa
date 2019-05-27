import attr
from marconpa.gui.utils import IdHandler


@attr.s(kw_only=True)
class CallbackHandler:

    idhandler = attr.ib(type=IdHandler, default=None)
    callback_property = attr.ib(type=IdHandler, default=None)
    callback_data = attr.ib(default=None)


    @classmethod
    def from_callback_context(cls, callback_id, callback_data):
        if "." in callback_id:
            component_id, callback_property = callback_id.split(".")
        else:
            component_id = callback_id
            callback_property = ""


        idhandler = IdHandler.from_id(component_id)
        return cls(idhandler=idhandler, callback_property=callback_property, callback_data=callback_data)

