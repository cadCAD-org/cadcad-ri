"""Blocks and Dynamics definitions."""

import functools
from typing import Any, Callable


def block(func: Callable) -> Callable:
    """_summary_

    Parameters
    ----------
    func : Callable
        _description_

    Returns
    -------
    Callable
        _description_
    """

    @functools.wraps(func)
    def wrapper_decorator(*args: Any, **kwargs: Any) -> Any:
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value * 2

    return wrapper_decorator
