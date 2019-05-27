def callback_tablechanged(table_data):
    """
    Callback reflecting changes in table onto the figure
    :param table_data:
    :return:
    """
    return {
        "data": [
            {"x": [row["x0"], row["x1"]], "y": [row["y0"], row["y1"]], "type": "line"}
            for row in table_data
        ]
    }


def callback_update_drwopdown_deleterows(input):
    length = len(input)
    options = []
    for i in range(length):
        options.append({"label":str(i), "value": i})

    return options

