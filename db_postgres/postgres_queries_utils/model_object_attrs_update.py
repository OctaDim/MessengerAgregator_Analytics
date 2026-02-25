from typing import Dict

from sqlalchemy.orm import DeclarativeBase


def update_model_obj_no_commit(
        orm_model_object: DeclarativeBase,
        new_update_data: Dict[str, any],
        log_update_data: bool = False,
        skip_invalid_attrs: bool = False
) -> DeclarativeBase:
    invalid_attributes = []
    valid_update_data = {}
    model_class_name = orm_model_object.__class__.__name__

    for cur_attr_name, cur_attr_val in new_update_data.items():
        if not hasattr(orm_model_object, cur_attr_name):
            invalid_attributes.append(cur_attr_name)
        else:
            valid_update_data[cur_attr_name] = cur_attr_val

    if log_update_data:
        print(f"\nmodel_class_name: {model_class_name}")
        for cur_attr, cur_value in new_update_data.items():
            if cur_attr in invalid_attributes:
                if skip_invalid_attrs:
                    attr_error_str = "[SKIPPED]"
                else:
                    attr_error_str = "[ERROR]"
            else:
                attr_error_str = ""
            print(f"{cur_attr} = {cur_value} {attr_error_str}")
        print(f"\n")

    if invalid_attributes and not skip_invalid_attrs:
        log_error = (f"DB Not existing model object attribute name(s) [ERROR]:\n"
                     f"invalid_attributes: {invalid_attributes}\n"
                     f"model_class_name: {model_class_name}\n"
                     f"model_object: {orm_model_object}\n")
        print(log_error)
        raise AttributeError(log_error)

    for attr_name, attr_value in valid_update_data.items():
        try:
            setattr(orm_model_object, attr_name, attr_value)
        except Exception as error:
            log_error = (f"DB Failed to set model object attribute [ERROR]: \n"
                         f"error: {error}\n"
                         f"attr_name: {attr_name}\n"
                         f"attr_value: {attr_value}\n"
                         f"model_class_name: {model_class_name}\n"
                         f"model_object: {orm_model_object}\n")
            print(log_error)
            raise
    return orm_model_object
