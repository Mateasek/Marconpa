import dash_table
from marconpa.gui.utils import IdHandler
from marconpa.utils.conversions import list2string

def attributes_table(attributes, parent_id):
    """
    Constructs table for waveform display
    :param id: Table ID
    :param setpoints: Setpoints from waveform to fill the table
    :return:
    """
    data = []
    table_id = IdHandler(name="table", kind="Attributes", parent=parent_id)
    for key, item in attributes.items():
        if isinstance(item, list):
           item = list2string(item)
        data.append({"attribute name": key, "value": str(item)})

    table = dash_table.DataTable(
        id=table_id.id,
        columns=[{"name": i, "id": i} for i in ["attribute name", "value"]],
        data=data,
        editable=True,
    )

    return table,  [table_id]
