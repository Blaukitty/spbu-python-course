from typing import Any, Callable


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Transforms a function into a curried version.
    
    Args:
        function: The function to be curried
        arity: The number of arguments the function expects
        
    Returns:
        A curried version of the input function
    """
    if arity < 0:
        raise ValueError('Arity have to be positive or zero')
    def curry(*args: Any, **kwargs: Any) -> Any:
        total = len(args) + len(kwargs)
        if arity < total:
            raise ValueError(f'Function expects {arity} arguments, but {total} were given')
        if arity == total:
            return function(*args, **kwargs)
        else:
            def new(*new_args: Any, **next_kwargs: Any) -> Any:
                all_ar = args + new_args
                all_kwa = kwargs.copy()
                all_kwa.update(next_kwargs)
                return curry(*all_ar, **all_kwa)
            return new
    return curry


def uncurry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Transforms a curried function back into normal form.
    
    Args:
        function: The curried function to uncurry
        arity: The number of arguments the original function expected
        
    Returns:
        An uncurried version of the input function
    """
    if arity < 0:
        raise ValueError('Arity have to be positive')
    def uncurry(*args: Any, **kwargs: Any) -> Any:
        total = len(args) + len(kwargs)
        if arity != total:
            raise ValueError(f'Function expects {arity} arguments, but {total} were given')
        res = function
        for ar in args:
            res = res(ar)
        if kwargs:
            res = res(**kwargs)
        return res
    return uncurry
