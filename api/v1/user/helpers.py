def add_attr(attr_name, attr_value, data, database):
    setattr(data, attr_name, attr_value)
    database.commit()
    database.refresh(data)

    return data


def delete_attr(attr_name, data, database):
    setattr(data, attr_name, None)
    database.commit()
    database.refresh(data)

    return data
