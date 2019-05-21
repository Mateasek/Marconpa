import dash_table
from marconpa.core.gui.utils import IdHandler

def attributes_table(attributes, parent_id):
    """
    Constructs table for waveform display
    :param id: Table ID
    :param setpoints: Setpoints from waveform to fill the table
    :return:
    """
    data = []
    table_id = IdHandler(name="table", component_type="Attributes", parent=parent_id)
    for key, item in attributes.items():
        data.append({"attribute name": key, "value": str(item)})
        if isinstance(item, list):
            data[-1]["value"] = data[-1]["value"].replace("[", "{")
            data[-1]["value"] = data[-1]["value"].replace("]", "}")

    table = dash_table.DataTable(
        id=table_id.id,
        columns=[{"name": i, "id": i} for i in ["attribute name", "value"]],
        data=data,
        editable=True,
    )

    return table, {"table": table_id}
