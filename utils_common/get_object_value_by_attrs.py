from typing import Union, Type, List, Any

from utils_common.exec_time_decorator import execution_time_decorator


@execution_time_decorator(in_seconds=False,
                          note="get_obj_value_by_attrs_chain",
                          exec_time_logging=True,
                          new_line_after=False)
def get_obj_value_by_attrs_chain(
        base_class_or_obj: Union[Type, object],
        all_attributes_chain: List[str]
) -> Any | None:
    if not base_class_or_obj:
        return None

    cur_chained_obj_val = base_class_or_obj
    for cur_attr in all_attributes_chain:
        if not hasattr(cur_chained_obj_val, cur_attr):
            return None
        cur_chained_obj_val = getattr(cur_chained_obj_val, cur_attr)

    return cur_chained_obj_val
