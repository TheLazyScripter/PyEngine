from typing import Union, Tuple, Mapping, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import event_system


def create_callback(target: type, *args: Optional[Tuple[any]], **kwargs: Optional[Mapping[any]]):
    return lambda: target(*args, **kwargs)