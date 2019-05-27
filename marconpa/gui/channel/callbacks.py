def callback_update_drwopdown_deleterows(input):
    length = len(input)
    options = []
    for i in range(length):
        options.append({"label":str(i), "value": i})

    return options